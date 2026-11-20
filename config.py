import json
from pathlib import Path

# Default configuration values
DEFAULT_CONFIG = {
    "accelerator_key": "right",
    "brake_key": "left",
    "forward_tilt_key": "none",
    "backward_tilt_key": "none",
    "game_window_title": "Hill Climb Racing",
    "mirror_preview": True,
    "swap_hand_labels": False,
    "send_keys_only_when_focused": True,
    "camera_index": -1,  # -1 means auto-detect
    "fps_target": 30,
    "max_camera_index": 4,
    "min_detection_confidence": 0.6,
    "min_tracking_confidence": 0.5,
    "model_complexity": 0,
    "finger_extend_ratio": 1.15,
    "thumb_extend_ratio": 1.0,
    "tilt_threshold_deg": 20,
    "tilt_deadzone_deg": 10,
    "pose_smoothing_frames": 5,
    "closed_fist_ratio": 0.35,
    "pose_stability_frames": 2,
    "angle_smoothing_factor": 0.5,
    "tracking_grace_frames": 2,
}

CONFIG_PATH = Path(__file__).with_name("settings.json")

def load_config():
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Merge with defaults to fill missing keys
            merged = {**DEFAULT_CONFIG, **data}
            return merged
        except Exception as e:
            print(f"Failed to load config: {e}, using defaults")
    return DEFAULT_CONFIG.copy()

def save_config(config):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Failed to save config: {e}")
