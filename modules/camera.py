"""camera.py – Handles webcam discovery, opening, frame capture and safe shutdown.
The implementation follows the specification in Phase 3:
* Scan indices 0‑4, trying DirectShow first (cv2.CAP_DSHOW on Windows).
* Verify that the camera opens and returns a frame.
* Provide `Camera` class with `start()`, `stop()`, `read()` and `rescan()`.
* Emit `CameraDisconnected` after 15 consecutive read failures.
* Mirrors frames horizontally when configured.
* Limits processing to a target FPS (default 30) by sleeping the remainder of the frame interval.
* All heavy work runs in a background thread; the UI can poll `latest_frame` and status flags.
"""
import cv2
import threading
import time
from typing import Optional, Tuple

from config import load_config

class CameraError(RuntimeError):
    pass

class CameraDisconnected(RuntimeError):
    pass

class Camera:
    def __init__(self):
        self.config = load_config()
        self.cap: Optional[cv2.VideoCapture] = None
        self.index: int = -1  # -1 means auto‑detect
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.latest_frame: Optional[object] = None  # will hold a numpy array
        self.failed_reads = 0
        self.lock = threading.Lock()
        self.fps_target = self.config.get("fps_target", 30)
        self.frame_interval = 1.0 / max(1, self.fps_target)
        self.mirror = self.config.get("mirror_preview", True)

    # ---------------------------------------------------------------------
    # Camera discovery & opening
    # ---------------------------------------------------------------------
    def _try_open(self, idx: int) -> Optional[cv2.VideoCapture]:
        """Attempt to open a camera at *idx*.
        On Windows we first try DirectShow (CAP_DSHOW) because it is faster and
        more reliable with built‑in webcams.
        """
        # DirectShow flag is only available on Windows; safely ignore on other OS.
        try:
            cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        except Exception:
            cap = cv2.VideoCapture(idx)
        if not cap.isOpened():
            return None
        # Verify that we can read a frame.
        ret, _ = cap.read()
        if not ret:
            cap.release()
            return None
        return cap

    def _detect_camera(self) -> Tuple[int, cv2.VideoCapture]:
        """Scan indices 0‑4 and return the first working camera.
        Raises `CameraError` if none are available.
        """
        max_idx = self.config.get("max_camera_index", 4)
        for i in range(max_idx + 1):
            cap = self._try_open(i)
            if cap:
                return i, cap
        raise CameraError("No reachable webcam found in indices 0‑%d" % max_idx)

    def start(self, index: int = -1) -> None:
        """Start the capture thread.
        *index* = -1 → auto‑detect, otherwise force a specific device.
        """
        if self.running:
            raise CameraError("Camera already running")
        self.index = index
        # Open the camera (auto‑detect or forced).
        if self.index == -1:
            idx, cap = self._detect_camera()
            self.index = idx
        else:
            cap = self._try_open(self.index)
            if not cap:
                raise CameraError(f"Camera index {self.index} could not be opened")
        self.cap = cap
        self.running = True
        self.failed_reads = 0
        self.thread = threading.Thread(target=self._run, daemon=True, name="CameraThread")
        self.thread.start()

    def stop(self) -> None:
        """Terminate the capture thread and release the device."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        with self.lock:
            if self.cap:
                self.cap.release()
            self.cap = None
            self.latest_frame = None
        self.thread = None

    # ---------------------------------------------------------------------
    # Background loop
    # ---------------------------------------------------------------------
    def _run(self) -> None:
        """Capture loop that respects the target FPS and mirrors frames if needed."""
        next_time = time.time()
        while self.running and self.cap:
            ret, frame = self.cap.read()
            if not ret:
                self.failed_reads += 1
                if self.failed_reads >= 15:
                    # Signal disconnection to callers.
                    self.running = False
                    raise CameraDisconnected("Camera lost after 15 consecutive read failures")
                # Skip this iteration – we still wait for the next frame interval.
            else:
                self.failed_reads = 0
                if self.mirror:
                    frame = cv2.flip(frame, 1)
                with self.lock:
                    self.latest_frame = frame
            # Sleep to keep roughly the target FPS.
            next_time += self.frame_interval
            sleep_dur = max(0.0, next_time - time.time())
            if sleep_dur > 0:
                time.sleep(sleep_dur)

    # ---------------------------------------------------------------------
    # Public accessor
    # ---------------------------------------------------------------------
    def read(self) -> Optional[object]:
        """Return the most recent frame (or ``None`` if not yet available)."""
        with self.lock:
            return self.latest_frame.copy() if self.latest_frame is not None else None

    def rescan(self) -> None:
        """Stop the current device (if any) and re‑detect the first working camera.
        Useful for the RESCAN button in the UI.
        """
        self.stop()
        # Reset index so that `_detect_camera` runs.
        self.index = -1
        self.start()

    # ---------------------------------------------------------------------
    # Convenience properties for UI
    # ---------------------------------------------------------------------
    @property
    def is_running(self) -> bool:
        return self.running

    @property
    def current_index(self) -> int:
        return self.index

    @property
    def last_failed_reads(self) -> int:
        return self.failed_reads

"""End of camera.py"""
