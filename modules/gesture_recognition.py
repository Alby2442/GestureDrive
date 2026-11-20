"""gesture_recognition.py – Detects high‑level hand gestures from MediaPipe landmarks.

The module provides a `GestureRecognizer` class that:
* Takes the raw pixel landmarks returned by `HandDetector`.
* Determines whether the hand is an **open palm**, **closed fist**, or **none/neutral**.
* Computes the roll angle of the hand (used for forward/backward tilt).
* Applies two layers of smoothing:
  - Pose smoothing by majority vote over the last `pose_smoothing_frames` frames.
  - Pose stability: a new pose must be observed for `pose_stability_frames` consecutive frames
    before it becomes the reported gesture (reduces flicker).
  - Angle smoothing via exponential moving average (`angle_smoothing_factor`).
* Returns a dict containing `gesture`, `tilt`, and `roll_angle`.
"""

import math
import collections
from typing import List, Dict, Optional

from .hand_utils import pick_right_hand
from config import load_config

# MediaPipe landmark indices (0‑20)
WRIST = 0
THUMB_TIP = 4
INDEX_TIP = 8
MIDDLE_TIP = 12
RING_TIP = 16
PINKY_TIP = 20
# MCP joints (base of each finger)
THUMB_MCP = 2
INDEX_MCP = 5
MIDDLE_MCP = 9
RING_MCP = 13
PINKY_MCP = 17

FINGER_TIPS = [INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP]
FINGER_MCP = [INDEX_MCP, MIDDLE_MCP, RING_MCP, PINKY_MCP]


class GestureRecognizer:
    def __init__(self):
        # Load configuration once – all other attributes depend on it.
        self.cfg = load_config()
        # History of raw pose classifications ("open_palm", "closed_fist", "none").
        self.pose_history = collections.deque(
            maxlen=self.cfg.get("pose_smoothing_frames", 3)
        )
        # Smoothed roll angle (EMA).
        self.smoothed_angle: Optional[float] = None
        self.angle_factor = self.cfg.get("angle_smoothing_factor", 0.5)
        # Tilt classification thresholds.
        self.tilt_threshold = self.cfg.get("tilt_threshold_deg", 20)
        self.tilt_deadzone = self.cfg.get("tilt_deadzone_deg", 10)
        # Stability parameters – avoid rapid flicker.
        self.pose_stability_frames = self.cfg.get("pose_stability_frames", 2)
        self.stability_counter = 0
        self.stable_pose: str = "none"
        # Configurable ratios for finger/thumb extension detection.
        self.finger_extend_ratio = self.cfg.get("finger_extend_ratio", 1.15)
        self.thumb_extend_ratio = self.cfg.get("thumb_extend_ratio", 1.0)
        self.closed_fist_ratio = self.cfg.get("closed_fist_ratio", 0.35)  # fraction of hand size

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def process(self, detections: List[Dict]) -> Dict:
        """Analyse a list of hand detections and return gesture information.

        The returned dict contains:
            - ``gesture``: "open_palm", "closed_fist" or "none"
            - ``tilt``: "forward", "backward" or "neutral"
            - ``roll_angle``: smoothed roll angle in degrees
        """
        # -------------------------------------------------------------
        # Select the right hand (respecting mirroring / swap settings)
        # -------------------------------------------------------------
        right = pick_right_hand(
            detections,
            mirrored=self.cfg.get("mirror_preview", True),
            swap=self.cfg.get("swap_hand_labels", False),
        )
        if not right:
            # No hand – clear histories and return neutral state.
            self.pose_history.clear()
            self.smoothed_angle = None
            self.stable_pose = "none"
            self.stability_counter = 0
            return {"gesture": "none", "tilt": "neutral", "roll_angle": 0.0}

        landmarks = right["landmarks"]  # list of (x, y) pixel tuples

        # -------------------------------------------------------------
        # 1️⃣ Raw pose classification (open / closed / none)
        # -------------------------------------------------------------
        raw_pose = self._classify_pose(landmarks)
        self.pose_history.append(raw_pose)
        # Majority‑vote smoothing over the history.
        smoothed_pose = max(set(self.pose_history), key=self.pose_history.count)

        # -------------------------------------------------------------
        # 2️⃣ Pose stability – require the same pose for a few frames.
        # -------------------------------------------------------------
        if smoothed_pose == self.stable_pose:
            self.stability_counter = 0
        else:
            self.stability_counter += 1
            if self.stability_counter >= self.pose_stability_frames:
                self.stable_pose = smoothed_pose
                self.stability_counter = 0
        final_gesture = self.stable_pose

        # -------------------------------------------------------------
        # 3️⃣ Roll angle (for tilt) with EMA smoothing
        # -------------------------------------------------------------
        roll = self._compute_roll_angle(landmarks)
        if self.smoothed_angle is None:
            self.smoothed_angle = roll
        else:
            self.smoothed_angle = (
                self.angle_factor * roll + (1 - self.angle_factor) * self.smoothed_angle
            )
        tilt = self._classify_tilt(self.smoothed_angle)

        return {
            "gesture": final_gesture,
            "tilt": tilt,
            "roll_angle": self.smoothed_angle,
        }

    # ---------------------------------------------------------------------
    # Helper methods
    # ---------------------------------------------------------------------
    @staticmethod
    def _distance(p1, p2) -> float:
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def _hand_size(self, lm: List[tuple]) -> float:
        """Robust hand‑size metric: distance between wrist and middle‑finger MCP.
        All distance‑based thresholds are expressed as a fraction of this size.
        """
        wrist = lm[WRIST]
        mcp_mid = lm[MIDDLE_MCP]
        return self._distance(wrist, mcp_mid)

    def _classify_pose(self, lm: List[tuple]) -> str:
        """Classify the hand as ``open_palm``, ``closed_fist`` or ``none``.

        The logic is based on relative finger tip positions:
        * **Open palm** – thumb tip is left of its MCP (for a right hand) *and* all four
          non‑thumb fingers have their tip above the corresponding MCP (smaller y).
        * **Closed fist** – thumb not extended and *either*:
            1. Every fingertip is within ``closed_fist_ratio`` × hand‑size of its MCP
               (strict distance check).
            2. Every fingertip lies below its MCP (larger y) – a generous fallback.
        Anything else returns ``none``.
        """
        # ----- thumb direction (swap flag may invert logic) -----
        thumb_tip = lm[THUMB_TIP]
        thumb_mcp = lm[THUMB_MCP]
        swap = self.cfg.get("swap_hand_labels", False)
        if swap:
            thumb_extended = thumb_tip[0] > thumb_mcp[0]  # inverted hand
        else:
            thumb_extended = thumb_tip[0] < thumb_mcp[0]  # normal right hand

        # ----- open‑palm detection -----
        extended_fingers = 0
        for tip_idx, mcp_idx in zip(FINGER_TIPS, FINGER_MCP):
            tip = lm[tip_idx]
            mcp = lm[mcp_idx]
            if tip[1] < mcp[1]:  # tip higher (smaller y) → extended
                extended_fingers += 1
        if thumb_extended and extended_fingers == 4:
            return "open_palm"

        # ----- closed‑fist detection -----
        hand_sz = self._hand_size(lm)
        strict_thresh = self.closed_fist_ratio * hand_sz
        all_strict_folded = all(
            self._distance(lm[tip_idx], lm[mcp_idx]) <= strict_thresh
            for tip_idx, mcp_idx in zip(FINGER_TIPS, FINGER_MCP)
        )
        if not thumb_extended and all_strict_folded:
            return "closed_fist"

        # Fallback: fingertips below their MCPs.
        all_below = all(lm[tip_idx][1] > lm[mcp_idx][1] for tip_idx, mcp_idx in zip(FINGER_TIPS, FINGER_MCP))
        if not thumb_extended and all_below:
            return "closed_fist"

        return "none"

    def _compute_roll_angle(self, lm: List[tuple]) -> float:
        """Calculate roll angle in degrees using wrist and middle‑MCP.
        Positive = clockwise (right rotation).
        """
        wrist = lm[WRIST]
        middle_mcp = lm[MIDDLE_MCP]
        vx = middle_mcp[0] - wrist[0]
        vy = middle_mcp[1] - wrist[1]
        # y axis points down in image coordinates.
        angle_rad = math.atan2(vx, -vy)
        return math.degrees(angle_rad)

    def _classify_tilt(self, angle: float) -> str:
        """Map a smoothed roll angle to a tilt direction.
        Returns ``forward``, ``backward`` or ``neutral``.
        """
        if abs(angle) <= self.tilt_deadzone:
            return "neutral"
        if angle > self.tilt_threshold:
            return "forward"
        if angle < -self.tilt_threshold:
            return "backward"
        return "neutral"

"""End of gesture_recognition.py"""
