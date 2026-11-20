import sys
import os
import cv2
import time

# Ensure the project root is on sys.path so imports work when executed directly.
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

from modules.camera import Camera
from modules.hand_detection import HandDetector
from modules.hand_utils import pick_right_hand
from modules.gesture_recognition import GestureRecognizer
from utils.fps_counter import FPSCounter
from config import load_config
from modules.keyboard_controller import KeyboardController

# Optional: Windows API for focus detection (requires pywin32)
try:
    import win32gui
except ImportError:
    win32gui = None


def is_hill_climb_focused() -> bool:
    """Return ``True`` if the active foreground window looks like the Hill Climb Racing game.

    The Microsoft Store version usually contains the phrase "Hill Climb Racing"
    in its window title. If ``win32gui`` is unavailable we fall back to ``True``
    so the program still works in environments without the dependency.
    """
    if win32gui is None:
        return True
    try:
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        return "Hill Climb Racing" in title
    except Exception:
        return False


def main(test_keys: bool = False):
    """Run the gesture detection loop.

    Args:
        test_keys: If ``True`` a separate window shows which arrow keys are
            currently pressed. The normal camera preview is still displayed.
    """
    cfg = load_config()
    cam = Camera()
    detector = HandDetector()
    recognizer = GestureRecognizer()
    fps_counter = FPSCounter(window_size=15)
    control_active = False  # toggled with 's'
    emergency_stop = False
    active_keys: set[str] = set()

    try:
        cam.start()
        print(
            f"Camera started on index {cam.current_index}. Press ESC to quit, 's' to toggle control, 'e' for emergency stop."
        )
        while cam.is_running:
            frame = cam.read()
            if frame is None:
                cv2.waitKey(30)
                continue

            # -----------------------------------------------------------------
            # Hand detection & gesture classification
            # -----------------------------------------------------------------
            detections = detector.detect(frame)
            gesture_info = recognizer.process(detections)
            right_hand = pick_right_hand(
                detections,
                mirrored=cfg.get("mirror_preview", True),
                swap=cfg.get("swap_hand_labels", False),
            )

            # Draw hand landmarks
            for det in detections:
                HandDetector.draw_hand(frame, det)

            # Handedness overlay
            cv2.putText(
                frame,
                "Right Hand Detected" if right_hand else "No Right Hand",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 0) if right_hand else (0, 0, 255),
                2,
                cv2.LINE_AA,
            )

            # -----------------------------------------------------------------
            # UI / dashboard status overlay (Phase 4)
            # -----------------------------------------------------------------
            # Control state
            control_text = "CONTROL ACTIVE" if control_active else "CONTROL OFF"
            cv2.putText(
                frame,
                control_text,
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 0) if control_active else (100, 100, 100),
                2,
                cv2.LINE_AA,
            )

            # Gesture‑to‑action overlay
            if gesture_info["gesture"] == "open_palm":
                gesture_text = "OPEN HAND – ACCELERATING"
                extra = "ACCELERATOR – RIGHT ARROW"
            elif gesture_info["gesture"] == "closed_fist":
                gesture_text = "CLOSED FIST – BRAKING"
                extra = "BRAKE – LEFT ARROW"
            else:
                gesture_text = "NO HAND DETECTED"
                extra = ""
            cv2.putText(
                frame,
                gesture_text,
                (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
            if extra:
                cv2.putText(
                    frame,
                    extra,
                    (10, 150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )

            # -----------------------------------------------------------------
            # Keyboard mapping – Phase 5 (game focus) & Phase 3 safety rules
            # -----------------------------------------------------------------
            if emergency_stop:
                # Emergency stop overrides everything.
                control_active = False
                KeyboardController.reset_all()
                active_keys.clear()
                emergency_stop = False
            elif control_active and is_hill_climb_focused():
                # Only send keys when control is on **and** the game window is focused.
                if gesture_info["gesture"] == "open_palm":
                    KeyboardController.press("right")
                    KeyboardController.release("left")
                    active_keys = {"right"}
                elif gesture_info["gesture"] == "closed_fist":
                    KeyboardController.press("left")
                    KeyboardController.release("right")
                    active_keys = {"left"}
                else:
                    KeyboardController.release("right")
                    KeyboardController.release("left")
                    active_keys.clear()
            else:
                # Ensure we never hold keys when control is off or game is unfocused.
                KeyboardController.release("right")
                KeyboardController.release("left")
                active_keys.clear()

            # -----------------------------------------------------------------
            # FPS overlay
            # -----------------------------------------------------------------
            fps = fps_counter.tick()
            cv2.putText(
                frame,
                f"FPS: {fps:.1f}",
                (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 0),
                2,
                cv2.LINE_AA,
            )

            # -----------------------------------------------------------------
            # Window handling
            # -----------------------------------------------------------------
            if test_keys:
                from utils.key_test_window import show_test_window
                show_test_window(frame, active_keys)
                cv2.imshow('GestureDrive Camera Preview', frame)
            else:
                cv2.imshow('GestureDrive Camera Preview', frame)

            # Capture key presses *after* windows have been refreshed.
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == ord('s'):
                control_active = not control_active
                print(f"Gesture control {'ENABLED' if control_active else 'DISABLED'}")
            elif key == ord('e'):
                emergency_stop = True
                print("Emergency STOP requested – keys will be released.")
    finally:
        KeyboardController.reset_all()
        cam.stop()
        detector.close()
        cv2.destroyAllWindows()
        print('Camera stopped.')

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='GestureDrive')
    parser.add_argument(
        '--test-keys', action='store_true', help='Run key‑test window instead of full preview'
    )
    args = parser.parse_args()
    main(test_keys=args.test_keys)
