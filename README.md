# GestureDrive

Hand Gesture Controlled Hill Climb Racing Game Using Python

**Drive with your hands. Conquer every hill.**

---

## Table of Contents
- [Introduction](#introduction)
- [Project Objectives](#project-objectives)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [How GestureDrive Works](#how-gesturedrive-works)
- [Gesture → Key Mapping](#gesture--key-mapping)
- [System Requirements](#system-requirements)
- [Windows Installation](#windows-installation)
- [Virtual Environment Setup](#virtual-environment-setup)
- [Dependency Installation](#dependency-installation)
- [Installation Verification](#installation-verification)
- [Running the Application](#running-application)
- [Project Directory Structure](#project-directory-structure)
- [Troubleshooting](#troubleshooting)
- [Screenshots \u0026 Demo GIF](#screenshots--demo-gif)
- [Future Improvements](#future-improvements)
- [Credits](#credits)
- [License](#license)

---

## Introduction
GestureDrive is a **Python‑based computer‑vision** application that enables hands‑free control of the classic *Hill Climb Racing* game. Using a standard laptop webcam, the program detects the user’s right hand, recognises open‑palm and closed‑fist gestures, and translates them into keyboard presses that drive the in‑game car.

---

## Project Objectives
- Provide a lightweight, real‑time hand‑gesture interface for an existing game.
- Keep the implementation pure Python with minimal external dependencies.
- Offer a clear, user‑friendly Tkinter dashboard for calibration and status.
- Ensure safe, deterministic key handling (press → release, emergency stop).

---

## Key Features
| Feature | Description |
|---|---|
| Real‑time webcam hand detection | Captures frames at up to 30 FPS, mirrors preview for intuitive control. |
| MediaPipe hand tracking | Utilises MediaPipe Hands (v0.10.21) for robust 21‑point landmark detection. |
| Open palm \u0026 closed fist recognition | Simple geometry‑based classification, independent of hand rotation. |
| Gesture smoothing \u0026 stability | Majority‑vote smoothing over recent frames and stability‑frame gating to eliminate flicker. |
| Keyboard control integration | Thin `pyautogui` wrapper sends `right` (accelerate) and `left` (brake) keys. |
| Hill Climb Racing window detection | Optional Windows API check (`win32gui`) ensures keys are sent only when the game is focused. |
| Tkinter control dashboard | Live preview, calibration wizard, status overlay, and emergency‑stop button. |
| Emergency stop | Press **E** (or click the dashboard button) to instantly release all keys. |
| FPS monitoring | On‑screen FPS counter helps evaluate performance. |

---

## Technologies Used
![Python](https://img.shields.io/badge/python-3.12%20|%203.11-blue) ![OpenCV](https://img.shields.io/badge/opencv-4.11.0.86-orange) ![MediaPipe](https://img.shields.io/badge/mediapipe-0.10.21-brightgreen) ![PyAutoGUI](https://img.shields.io/badge/pyautogui-0.9.54-lightgrey) ![Tkinter](https://img.shields.io/badge/Tkinter‑builtin‑purple)

- **Python 3.12** (Windows installer) 
- **OpenCV‑contrib‑python** – for video capture \u0026 image display. 
- **MediaPipe** – hand‑landmark detection. 
- **NumPy** – numeric arrays used by OpenCV \u0026 MediaPipe. 
- **PyAutoGUI** – cross‑platform keyboard automation. 
- **Tkinter** – native GUI for the dashboard. 
- **Optional:** `pywin32` (window‑title focus detection) / `pydirectinput` (alternative key‑sending backend).

---

## How GestureDrive Works
1. **Camera Thread** – `modules.camera.Camera` discovers a working webcam (indices 0‑4), mirrors frames, and supplies the latest frame at a target FPS (default 30). 
2. **Hand Detection** – `modules.hand_detection.HandDetector` runs MediaPipe on each frame and returns a list of detected hands with landmarks. 
3. **Right‑Hand Selection** – `modules.hand_utils.pick_right_hand` picks the right hand, optionally swapping labels per user setting. 
4. **Gesture Classification** – `modules.gesture_recognition.GestureRecognizer` analyses landmarks, applies smoothing, and outputs a high‑level gesture (`open_palm`, `closed_fist`, `none`) plus tilt information. 
5. **Keyboard Controller** – `modules.keyboard_controller.KeyboardController` presses/release the mapped keys only while **control is active** and the game window is focused. 
6. **Dashboard** – Tkinter UI shows live preview, FPS, current gesture, and status indicators; the user can toggle control (**S**) and invoke an emergency stop (**E**).

---

## Gesture → Key Mapping
| Gesture / Input | Key Sent | Action |
|---|---|---|
| **Open Palm** | `right` | Accelerate (hold) |
| **Closed Fist** | `left` | Brake (hold) |
| **No recognized gesture** | – | Release all controls |
| **S** | – | Toggle control on/off |
| **E** | – | Emergency stop – release every key |
| **ESC** | – | Exit the application |

\u003e *Note:* The exact key symbols are configurable in `config.py` / `settings.json`.

---

## System Requirements
- Windows 11 (or Windows 10) 64‑bit
- Python 3.12 (official installer, include *tcl/tk* for Tkinter)
- Laptop webcam with at least 720 p resolution
- Minimum 4 GB RAM (more recommended for smooth UI)

---

## Windows Installation
```powershell
# 1️⃣ Clone / copy the repository to a local folder, e.g. C:\\SchoolProject\\GestureDrive
# 2️⃣ Open PowerShell in that folder
# 3️⃣ (Optional) Bypass script‑execution policy for this session
Set-ExecutionPolicy -Scope Process Bypass
```
\u003e If you prefer Command Prompt, use the corresponding `activate.bat` script instead of the PowerShell `activate` script.

---

## Virtual Environment Setup
```powershell
# Create a clean virtual environment named \"venv\"
python -m venv venv
# Activate it (PowerShell)
.\\venv\\Scripts\\Activate
# Or activate in CMD
venv\\Scripts\\activate.bat
```

---

## Dependency Installation
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
# Optional dependencies (only if you need them)
# python -m pip install pywin32        # for window‑title focus detection
# python -m pip install pydirectinput  # alternative backend for games that block pyautogui
```

---

## Installation Verification
```powershell
python check_install.py
```
The script should finish with **All good.** If any import errors appear, reinstall the failing package.

---

## Running the Application
```powershell
python main.py
```
* The webcam preview window appears. Press **S** to enable control, **E** for emergency stop, and **ESC** to quit.

---

## Project Directory Structure
```
GestureDrive/                # repository root
├── main.py                # entry point (no changes required)
├── config.py              # default settings \u0026 loader
├── requirements.txt
├── check_install.py
├── README.md
├── .gitignore            # (added by this guide)
├── modules/               # core logic
│   ├── camera.py
│   ├── hand_detection.py
│   ├── hand_utils.py
│   ├── gesture_recognition.py
│   ├── keyboard_controller.py
│   ├── calibration.py
│   └── engine.py
├── interface/
│   └── dashboard.py
├── utils/
│   ├── fps_counter.py
│   └── key_test_window.py
├── assets/
│   └── icons/app_icon.png   # application icon (not ignored)
├── tests/                 # unit / integration tests
│   ├── test_camera.py
│   ├── test_gesture.py
│   �... (truncated for brevity) ...
```

---

## Troubleshooting
| Problem | Suggested Fix |
|---|---|
| **No working camera found** | Close other apps using the webcam, ensure Windows privacy settings allow camera access, click **RESCAN** in the dashboard. |
| **mediapipe import error** | Install the exact version: `python -m pip install mediapipe==0.10.21`. |
| **Both `opencv-python` and `opencv-contrib-python` installed** | Uninstall `opencv-python` (`python -m pip uninstall -y opencv-python`) and reinstall from `requirements.txt`. |
| **Gesture works but game receives no input** | Verify the game window title matches the value in the dashboard, confirm the mapped keys match the game controls, or try the alternative backend `pydirectinput`. |
| **Left hand controls the car** | Enable the **Swap left/right hand labels** option in the dashboard. |
| **Tilt direction reversed** | Re‑calibrate after toggling the **Mirror preview** setting. |
| **Application crashes on startup** | Run `check_install.py` again, ensure the virtual environment is activated, and double‑check Python version (3.12). |

---

## Visual Preview – Coming Soon

\u003e Visual assets (branding banner, demo GIF, and UI screenshots) are being prepared. Stay tuned for updates.

---

## Future Improvements
- Add support for custom key‑mapping profiles (per‑game). 
- Provide a lightweight CLI mode (no Tkinter UI). 
- Implement tilt‑based steering (forward/backward keys). 
- Package as a single‑file executable for easier distribution. 

---

## Credits
- **Author:** *Your Name* (feel free to add contributors). 
- **MediaPipe** – Google’s cross‑platform ML solutions. 
- **OpenCV** – Open‑source computer‑vision library. 
- **PyAutoGUI** – Keyboard‑automation library. 
- **Tkinter** – Standard Python GUI toolkit.

---

## License
*License placeholder – choose an appropriate open‑source license (e.g., MIT, Apache 2.0) before publishing.*
