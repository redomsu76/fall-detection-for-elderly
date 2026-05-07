# Elderly Fall Detection & Active Alert System (Local Run Example)

=============================
Part 1: How to Run (Get It Working First)
=============================

## 1. What This Project Does
--------------------------------
This is an example project for learning and research. Its goals are:

- Detect possible falls of an elderly person via a webcam
- Recognize calls for help via microphone
- Send alert notifications to a mobile phone when an abnormal event is detected

### Key Features:
- Runs fully locally, no cloud services required
- Designed for technical learning and experimentation
- Not a medical device, nor a safety guarantee system


## 2. Runtime Environment
-------------------------
- Windows 10 / Windows 11
- Python 3.10 (Python 3.12 is NOT recommended)
- USB webcam
- Microphone


## 3. First-Time Setup (Step by Step)
---------------------------------------
1. Open the project folder
2. Hold `Shift` and right-click in the blank area
3. Select "Open PowerShell window here"

Then run the following three commands, one by one:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt