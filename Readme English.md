# Elderly Fall Detection & Active Alert System (Local Run Example)

=============================
## Part 1: How to Run (Get It Working First)
=============================

### 1. What This Project Does

This is an example project for learning and research. Its goals are:

- Detect possible falls of an elderly person via a webcam
- Recognize calls for help via microphone
- Send alert notifications to a mobile phone when an abnormal event is detected

**Key Features:**
- Runs fully locally, no cloud services required
- Designed for technical learning and experimentation
- Not a medical device, nor a safety guarantee system


### 2. Runtime Environment

- Windows 10 / Windows 11
- Python 3.10 (Python 3.12 is NOT recommended)
- USB webcam
- Microphone


### 3. First-Time Setup (Step by Step)

1. Open the project folder
2. Hold `Shift` and right-click in the blank area
3. Select "Open PowerShell window here"

Then run the following three commands, one by one:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
4. Configuration
Go to the config folder

Copy config.example.yaml

Rename the copy to config.yaml

Fill in the push notification settings as instructed
(You can skip this for your first learning run)

5. Run the Program
In the PowerShell window, type:

bash
python src/main.py
If the camera preview opens successfully, the program is running as expected.

=============================

Part 2: Learning Guide (Understanding & Modifying)
=============================

6. How the System Works (3–5 minutes)
When the program runs, it repeatedly does three things:

Watch the camera feed

Listen to the microphone

Decide whether to trigger an alert

The entire system is orchestrated by main.py. Other modules each have their own specific role.

7. Project Structure (with modification notes)
text
src/
 ├─ main.py            ★ Best starting point for reading
 ├─ camera.py          △ Not recommended for first changes
 ├─ fall_detect.py     ★ Best starting point for modifications
 ├─ audio_help.py      ★ Good for your second modification
 ├─ alert/
 │   ├─ telegram.py
 │   ├─ wechat.py
 │   └─ sms.py         ★ Good for practicing adding constraints
 └─ utils/             △ Can be reviewed later

config/
 ├─ config.example.yaml
 └─ config.yaml

models/                △ Not recommended to modify
requirements.txt       △ Not recommended to modify
README.txt
8. What to Modify First (Strongly recommended in this order)
fall_detect.py: Adjust thresholds, add consecutive-frame checks, add console status prints

main.py: Add logging, timestamps, and status indicators

alert/: Add cooldown timers or new notification methods

9. Parts Not Recommended for Modification
The models/ directory

requirements.txt

Camera initialization logic

The program's startup and exit flow

10. Learning Suggestions
Get it running first, then focus on understanding

Change only one small thing at a time

Run the program immediately after each change and observe the effect

Don't try to understand everything all at once

11. Purpose and Limitations
This project is intended only for learning and experimentation

It is NOT a medical device or a safety‑critical system
