# 安装依赖：
# pip install SpeechRecognition pyaudio

import cv2
import mediapipe as mp
import math
from collections import deque
import time
import threading
import speech_recognition as sr
import requests
import os

# -------------------------------
# 1️⃣ 房间选择
# -------------------------------
def select_room_type():
    print("请选择摄像头所在房间：")
    print("1 = 起居室 / 活动区")
    print("2 = 卧室")
    print("3 = 厕所 / 卫生间")

    choice = input("输入 1 / 2 / 3 然后回车：").strip()
    if choice == "1":
        return "living"
    elif choice == "2":
        return "bedroom"
    elif choice == "3":
        return "bathroom"
    else:
        print("输入错误，默认使用起居室")
        return "living"

ROOM_PARAMS = {
    "living": {"angle_thresh": 55, "still_time": 1.5},
    "bedroom": {"angle_thresh": 70, "still_time": 2.5},
    "bathroom": {"angle_thresh": 45, "still_time": 1.2}
}

# -------------------------------
# 2️⃣ 自适应学习
# -------------------------------
motion_history = deque(maxlen=120)
def adaptive_adjust(base_value, history, ratio=0.15):
    if len(history) < 30:
        return base_value
    avg = sum(history) / len(history)
    return base_value * (1 - ratio) + avg * ratio

# -------------------------------
# 3️⃣ 空间自适应
# -------------------------------
SPACE_SCALE = {"small": 0.85, "medium": 1.0, "large": 1.15}
def estimate_space_scale(landmarks, frame_height):
    try:
        head_y = landmarks[0].y
        ankle_y = (landmarks[27].y + landmarks[28].y) / 2
        return abs(ankle_y - head_y)
    except:
        return None
def classify_space(body_ratio):
    if body_ratio is None:
        return "unknown"
    if body_ratio > 0.75: return "small"
    elif body_ratio > 0.45: return "medium"
    else: return "large"

# -------------------------------
# 4️⃣ 警报机制
# -------------------------------
ALERT_COOLDOWN = 10
last_alert_time = 0

# Telegram 示例（可以替换成微信或短信接口）
TELEGRAM_BOT_TOKEN = "你的BOT_TOKEN"
TELEGRAM_CHAT_ID = "你的CHAT_ID"

def send_alert(message, image_path=None):
    global last_alert_time
    now = time.time()
    if now - last_alert_time < ALERT_COOLDOWN:
        return
    last_alert_time = now
    print("触发报警:", message)

    # Telegram 文字
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})
        if image_path and os.path.exists(image_path):
            url_file = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
            with open(image_path, "rb") as f:
                requests.post(url_file, data={"chat_id": TELEGRAM_CHAT_ID}, files={"photo": f})
    except Exception as e:
        print("发送 Telegram 失败：", e)

# -------------------------------
# 5️⃣ 语音呼救识别线程
# -------------------------------
def voice_alert_listener():
    r = sr.Recognizer()
    mic = sr.Microphone()
    while True:
        try:
            with mic as source:
                audio = r.listen(source, phrase_time_limit=3)
            text = r.recognize_google(audio, language="zh-CN")
            if "救命" in text or "help" in text.lower():
                send_alert("⚠️ 语音检测到呼救！")
        except:
            pass

# -------------------------------
# Mediapipe 初始化
# -------------------------------
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# -------------------------------
# 主程序
# -------------------------------
def main():
    room_type = select_room_type()
    print(f"当前房间类型：{room_type}")
    params = ROOM_PARAMS[room_type]

    # 启动语音监听线程
    threading.Thread(target=voice_alert_listener, daemon=True).start()

    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break

            frame = cv2.flip(frame, 1)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            status = "Normal"

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                space_ratio = estimate_space_scale(results.pose_landmarks.landmark, frame.shape[0])
                space_type = classify_space(space_ratio)
                scale = SPACE_SCALE.get(space_type, 1.0)

                left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
                right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
                right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]

                dx = ((left_shoulder.x+right_shoulder.x)/2) - ((left_hip.x+right_hip.x)/2)
                dy = ((left_shoulder.y+right_shoulder.y)/2) - ((left_hip.y+right_hip.y)/2)
                angle = math.degrees(math.atan2(dy, dx))

                motion_history.append(abs(angle))
                angle_thresh = adaptive_adjust(params["angle_thresh"], motion_history)
                angle_thresh *= scale

                if abs(angle) >= angle_thresh:
                    status = "Possible Fall!"
                    alert_image_path = "fall_alert.jpg"
                    cv2.imwrite(alert_image_path, frame)
                    send_alert("⚠️ 检测到可能摔倒！", alert_image_path)

            cv2.putText(image, f"Status: {status}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255) if status != "Normal" else (0, 255, 0), 2)
            cv2.imshow('Fall Detection', image)

            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
