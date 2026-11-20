# demo_detection.py – Live verification of gestures
import cv2, sys, os

# Make project root importable (same trick used in the tests)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from modules.camera import Camera
from modules.hand_detection import HandDetector
from modules.gesture_recognition import GestureRecognizer

def main():
    cam = Camera()
    cam.start()  # start the capture thread
    cam.start()  # start capture thread
    cam.start()  # start capture thread
    detector = HandDetector()
    recognizer = GestureRecognizer()

    print("Demo running – show gestures to the camera. Press ESC to quit.")
    while True:
        frame = cam.read()
        if frame is None:
            continue

        detections = detector.detect(frame)

        if detections:
            result = recognizer.process(detections)
            label = f"{result['gesture']} ({result['tilt']})"
            detector.draw_landmarks(frame, detections[0])
        else:
            label = "no hand"

        cv2.putText(frame, label, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                    (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("GestureDrive – Demo (ESC to quit)", frame)

        if cv2.waitKey(1) & 0xFF == 27:   # ESC key
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()