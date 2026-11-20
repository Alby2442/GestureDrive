"""hand_detection.py – wraps MediaPipe Hands for right‑hand detection.

The module provides a simple `HandDetector` class that:
* Initializes MediaPipe with the exact parameters required by the spec.
* Accepts a BGR OpenCV frame (already mirrored if configured).
* Converts it to RGB, runs MediaPipe, and returns a list of detected hands.
* Each hand entry contains:
    - `handedness` ("Right" or "Left")
    - `landmarks` – a list of 21 (x, y) pixel coordinates in the original frame size.
    - `world_landmarks` – optional 3‑D coordinates (not used yet).
* Offers a static `draw_hand` helper that draws the 21 landmarks and connections
  on a supplied frame using OpenCV drawing primitives.
"""
import cv2
import mediapipe as mp
from typing import List, Dict, Tuple


class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            model_complexity=0,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.5,
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_draw.DrawingSpec(thickness=2, circle_radius=2)

    def detect(self, frame: "numpy.ndarray") -> List[Dict]:
        """Detect hands in a BGR frame.

        Returns a list of dictionaries, one per detected hand, with the keys:
        * `handedness` – "Right" or "Left"
        * `landmarks` – list of 21 (x, y) pixel tuples
        * `world_landmarks` – list of 21 (x, y, z) tuples (optional)
        """
        # Convert BGR -> RGB as required by MediaPipe
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        detections = []
        if not results.multi_hand_landmarks:
            return detections
        for hand_landmarks, handedness in zip(
            results.multi_hand_landmarks, results.multi_handedness
        ):
            # Convert normalized landmarks to pixel coordinates
            h, w, _ = frame.shape
            pts = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]
            world_pts = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
            detections.append(
                {
                    "handedness": handedness.classification[0].label,
                    "landmarks": pts,
                    "world_landmarks": world_pts,
                    "mp_landmarks": hand_landmarks,  # keep original for drawing
                }
            )
        return detections

    @staticmethod
    def draw_hand(frame: "numpy.ndarray", hand_info: Dict) -> None:
        """Draw the hand landmarks and connections onto `frame`.
        The function mutates the frame in‑place.
        """
        mp_draw = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands
        mp_draw.draw_landmarks(
            frame,
            hand_info["mp_landmarks"],
            mp_hands.HAND_CONNECTIONS,
            mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            mp_draw.DrawingSpec(color=(0, 0, 255), thickness=2),
        )

    def close(self):
        self.hands.close()

"""End of hand_detection.py"""
