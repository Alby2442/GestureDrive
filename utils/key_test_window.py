import cv2
import numpy as np

def show_test_window(frame, pressed_keys):
    """Display a simple black window with the currently pressed keys.
    `pressed_keys` is a set of key names (e.g., "right", "left").
    """
    # Create a black canvas
    canvas = np.zeros((200, 400, 3), dtype=np.uint8)
    # Show pressed keys as text
    y = 30
    for key in sorted(pressed_keys):
        cv2.putText(
            canvas,
            f"Key down: {key}",
            (10, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )
        y += 30
    if not pressed_keys:
        cv2.putText(
            canvas,
            "No keys pressed",
            (10, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )
    cv2.imshow('Key Test', canvas)
    # Also forward the original camera frame (optional) – not displayed in test mode
    _ = frame
    # Wait a short time for the window to refresh

