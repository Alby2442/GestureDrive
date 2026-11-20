# modules/keyboard_controller.py – thin wrapper around pyautogui
# -----------------------------------------------------
# Provides press/release helpers and tracks currently held keys.
# -----------------------------------------------------
import pyautogui

# Disable built‑in pause and failsafe (so calls are immediate and never abort on mouse corner).
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False


class KeyboardController:
    """Utility to press/release keys while remembering which keys are held."""
    _pressed = set()

    @staticmethod
    def press(key: str) -> None:
        """Hold down *key* if not already held."""
        if key not in KeyboardController._pressed:
            pyautogui.keyDown(key)
            KeyboardController._pressed.add(key)

    @staticmethod
    def release(key: str) -> None:
        """Release *key* if it is currently held."""
        if key in KeyboardController._pressed:
            pyautogui.keyUp(key)
            KeyboardController._pressed.remove(key)

    @staticmethod
    def reset_all() -> None:
        """Release any key that might still be down – call on program exit."""
        for k in list(KeyboardController._pressed):
            pyautogui.keyUp(k)
        KeyboardController._pressed.clear()
