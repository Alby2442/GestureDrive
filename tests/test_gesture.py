# test_gesture.py – Unit tests for the GestureRecognizer.
# These tests use synthetic landmark data generated in `tests/synthetic.py` to verify
# that the recognizer classifies each pose correctly.

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.gesture_recognition import GestureRecognizer
from tests.synthetic import (
    open_palm,
    closed_fist,
    tilt_right,
    tilt_left,
    single_finger,
)

import unittest

def make_detection(landmarks, handedness="Right"):
    """Wrap raw landmarks into the dict format expected by GestureRecognizer.
    The recognizer only uses the ``handedness`` and ``landmarks`` fields.
    """
    return {
        "handedness": handedness,
        "landmarks": landmarks,
        "world_landmarks": [],
        "mp_landmarks": None,
    }

class TestGestureRecognition(unittest.TestCase):
    def setUp(self):
        self.recognizer = GestureRecognizer()

    def test_open_palm(self):
        det = make_detection(open_palm())
        result = self.recognizer.process([det])
        self.assertEqual(result["gesture"], "open_palm")
        self.assertEqual(result["tilt"], "neutral")

    def test_closed_fist(self):
        det = make_detection(closed_fist())
        result = self.recognizer.process([det])
        self.assertEqual(result["gesture"], "closed_fist")
        self.assertEqual(result["tilt"], "neutral")

    def test_tilt_right(self):
        det = make_detection(tilt_right())
        result = self.recognizer.process([det])
        # Open palm should be detected, tilt should be forward.
        self.assertEqual(result["gesture"], "open_palm")
        self.assertEqual(result["tilt"], "forward")

    def test_tilt_left(self):
        det = make_detection(tilt_left())
        result = self.recognizer.process([det])
        self.assertEqual(result["gesture"], "open_palm")
        self.assertEqual(result["tilt"], "backward")

    def test_single_finger_neutral(self):
        det = make_detection(single_finger())
        result = self.recognizer.process([det])
        self.assertEqual(result["gesture"], "none")
        self.assertEqual(result["tilt"], "neutral")

if __name__ == "__main__":
    unittest.main()
