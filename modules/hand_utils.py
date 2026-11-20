"""hand_utils.py – helper utilities for hand detection.

The core helper required by the specification is ``pick_right_hand`` which selects the
right‑hand detection from a list of MediaPipe candidates, taking into account the
``mirrored`` preview setting and the optional ``swap_hand_labels`` configuration.

The function is pure‑Python and unit‑testable without any MediaPipe runtime.
"""
from typing import List, Optional, Dict


def _invert_label(label: str) -> str:
    """Return the opposite handedness label.
    MediaPipe uses "Right" / "Left" strings.
    """
    return "Left" if label == "Right" else "Right" if label == "Left" else label


def pick_right_hand(
    candidates: List[Dict],
    mirrored: bool = False,
    swap: bool = False,
) -> Optional[Dict]:
    """Select the detection that corresponds to the **right** hand.

    Parameters
    ----------
    candidates
        List of detection dictionaries as produced by :class:`HandDetector`.
        Each dict must contain the key ``"handedness"`` with the value ``"Right"``
        or ``"Left"`` (the raw MediaPipe label).
    mirrored
        ``True`` if the preview is horizontally mirrored.  MediaPipe’s handedness
        is based on the *actual* hand, so mirroring does **not** change the label.
        The flag is kept for future extensions and for symmetry with the spec.
    swap
        If ``True`` the user has indicated that left/right labels should be swapped
        (UI option).  In that case we simply invert the MediaPipe label before
        deciding which hand is right.

    Returns
    -------
    dict or None
        The candidate representing the right hand, or ``None`` if no right hand
        is present.
    """
    for cand in candidates:
        label = cand.get("handedness")
        if not label:
            continue
        # Apply user‑level swap if requested.
        if swap:
            label = _invert_label(label)
        # ``mirrored`` does not affect the label (MediaPipe already knows the
        # physical hand), but we keep the argument for API compatibility.
        if label == "Right":
            return cand
    return None
"""End of hand_utils.py"""
