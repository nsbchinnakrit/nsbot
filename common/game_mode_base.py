# common/game_mode_base.py
import time, subprocess, logging

class GameModeBase:
    def __init__(self, pid, total, idle_minutes=1):
        self._pid = pid
        self._total = total
        self._last_activity = time.monotonic()
        self._idle_threshold = idle_minutes * 60

    def reset_idle_timer(self):
        self._last_activity = time.monotonic()

    def check_idle(self):
        if time.monotonic() - self._last_activity >= self._idle_threshold:
            logging.info(f"Idle > {self._idle_threshold}s, exiting.")
            self.create_file(str(self._total))
            subprocess.run(
                ['taskkill','/F','/PID', str(self._pid)],
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return True
        return False

    def run_loop(self):
        while True:
            if self.detect_something():
                self.reset_idle_timer()
            if self.check_idle():
                break

    def detect_something(self):
        raise NotImplementedError
