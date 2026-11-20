import time

class FPSCounter:
    """Simple FPS counter using a moving average over the last N frames.
    """
    def __init__(self, window_size: int = 10):
        self.window_size = max(1, window_size)
        self.times = []  # timestamps of recent frames

    def tick(self) -> float:
        """Call this each time a new frame is processed.
        Returns the current FPS estimate.
        """
        now = time.time()
        self.times.append(now)
        # keep only recent timestamps
        while len(self.times) > self.window_size:
            self.times.pop(0)
        if len(self.times) < 2:
            return 0.0
        elapsed = self.times[-1] - self.times[0]
        return (len(self.times) - 1) / elapsed if elapsed > 0 else 0.0
