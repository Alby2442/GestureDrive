"""synthetic.py – Helper functions to generate simple synthetic hand landmark sets for unit tests.
The coordinates are arbitrary pixel values; only relative positions matter for the
gesture recognition logic (y‑axis downwards, x‑axis rightwards).
"""
from typing import List, Tuple

# Landmark indices (same as MediaPipe)
WRIST = 0
THUMB_TIP = 4
THUMB_MCP = 2
INDEX_TIP = 8
INDEX_MCP = 5
MIDDLE_TIP = 12
MIDDLE_MCP = 9
RING_TIP = 16
RING_MCP = 13
PINKY_TIP = 20
PINKY_MCP = 17

def base_hand() -> List[Tuple[int, int]]:
    """Return a base hand (all joints at a neutral open position)."""
    return [(0, 0) for _ in range(21)]

def open_palm(right: bool = True) -> List[Tuple[int, int]]:
    """Generate landmarks for an open palm.
    All finger tips are above (smaller y) their MCPs. Thumb tip is left of MCP for a right hand.
    """
    lm = base_hand()
    lm[WRIST] = (100, 200)
    for idx in [THUMB_MCP, INDEX_MCP, MIDDLE_MCP, RING_MCP, PINKY_MCP]:
        lm[idx] = (100, 180)
    lm[THUMB_TIP] = (80, 150)  # left of MCP for right hand
    lm[INDEX_TIP] = (110, 150)
    lm[MIDDLE_TIP] = (120, 150)
    lm[RING_TIP] = (130, 150)
    lm[PINKY_TIP] = (140, 150)
    if not right:
        def mirror(x):
            return 200 - x
        for i in range(21):
            x, y = lm[i]
            lm[i] = (mirror(x), y)
    return lm

def closed_fist(right: bool = True) -> List[Tuple[int, int]]:
    """Generate landmarks for a closed fist.
    All finger tips are below (greater y) their MCPs. Thumb tip is right of MCP for a right hand.
    """
    lm = base_hand()
    lm[WRIST] = (100, 200)
    for idx in [THUMB_MCP, INDEX_MCP, MIDDLE_MCP, RING_MCP, PINKY_MCP]:
        lm[idx] = (100, 180)
    lm[THUMB_TIP] = (120, 210)  # right of MCP for right hand
    lm[INDEX_TIP] = (110, 210)
    lm[MIDDLE_TIP] = (120, 210)
    lm[RING_TIP] = (130, 210)
    lm[PINKY_TIP] = (140, 210)
    if not right:
        def mirror(x):
            return 200 - x
        for i in range(21):
            x, y = lm[i]
            lm[i] = (mirror(x), y)
    return lm

def tilt_right(right: bool = True) -> List[Tuple[int, int]]:
    """Generate landmarks for a clockwise‑rotated hand (positive roll)."""
    lm = open_palm(right)
    lm[MIDDLE_MCP] = (130, 180)  # x > wrist x creates positive roll
    return lm

def tilt_left(right: bool = True) -> List[Tuple[int, int]]:
    """Generate landmarks for a counter‑clockwise‑rotated hand (negative roll)."""
    lm = open_palm(right)
    lm[MIDDLE_MCP] = (70, 180)   # x < wrist x creates negative roll
    return lm

def single_finger(right: bool = True) -> List[Tuple[int, int]]:
    """Only the index finger is extended; others folded.
    Should be classified as `none` (neutral) for gas release.
    """
    lm = closed_fist(right)
    lm[INDEX_TIP] = (110, 150)  # above MCP
    return lm
