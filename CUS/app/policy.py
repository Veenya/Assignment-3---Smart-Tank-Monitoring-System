# Made by ChatGPT

from __future__ import annotations
from dataclasses import dataclass
from time import time
from typing import Optional, Tuple

from .state import SharedState, SystemMode


@dataclass
class PolicyConfig:
    # thresholds in % (0..100)
    L1: float = 60.0
    L2: float = 85.0

    # timings in seconds
    T1: float = 5.0    # must stay above L1 for >T1 to open 50%
    T2: float = 10.0   # no data for >T2 => UNCONNECTED

    # openings
    OPEN_0: int = 0
    OPEN_50: int = 50
    OPEN_100: int = 100


class Policy:
    """
    Implements the CUS behavior:
    - AUTOMATIC: compute desired valve opening based on water level and timers
    - MANUAL: desired opening is set externally (DBS/WCS)
    - UNCONNECTED: if no MQTT data for >T2, enter UNCONNECTED and go to safe opening (0)
    """
    def __init__(self, cfg: PolicyConfig):
        self.cfg = cfg
        self._above_L1_since: Optional[float] = None

    def _compute_automatic_opening(self, level: float) -> int:
        # L2: immediate full open
        if level >= self.cfg.L2:
            self._above_L1_since = None
            return self.cfg.OPEN_100

        # Between L1 and L2: open 50% only if level stays above L1 for T1
        if level >= self.cfg.L1:
            if self._above_L1_since is None:
                self._above_L1_since = time()
            if time() - self._above_L1_since >= self.cfg.T1:
                return self.cfg.OPEN_50
            return self.cfg.OPEN_0  # still waiting for T1
        else:
            # Below L1: close and reset timer
            self._above_L1_since = None
            return self.cfg.OPEN_0

    def tick(self, st: SharedState) -> Tuple[bool, Optional[str]]:
        """
        Returns (should_send_to_wcs, reason).
        Call this periodically (e.g., 10 times per second).
        """
        now = time()
        snap = st.snapshot()

        # UNCONNECTED check: no MQTT data for >T2
        last_ts = snap["last_level_ts"]
        if last_ts is None or (now - last_ts > self.cfg.T2):
            if snap["mode"] != SystemMode.UNCONNECTED.value:
                st.set_mode(SystemMode.UNCONNECTED)
                st.set_desired_opening(self.cfg.OPEN_0)
                return True, "enter_unconnected"
            # already unconnected: keep safe close
            if snap["desired_opening"] != self.cfg.OPEN_0:
                st.set_desired_opening(self.cfg.OPEN_0)
                return True, "unconnected_force_close"
            return False, None

        # If data is back and we were UNCONNECTED, return to AUTOMATIC by default
        if snap["mode"] == SystemMode.UNCONNECTED.value:
            st.set_mode(SystemMode.AUTOMATIC)
            # fallthrough to apply automatic opening immediately

        # AUTOMATIC policy
        if st.mode == SystemMode.AUTOMATIC:
            level = snap["tank_level"]
            if level is None:
                return False, None
            new_open = self._compute_automatic_opening(float(level))
            if new_open != snap["desired_opening"]:
                st.set_desired_opening(new_open)
                return True, "auto_open_change"
            return False, None

        # MANUAL: do nothing here (opening comes from DBS/WCS)
        if st.mode == SystemMode.MANUAL:
            return False, None

        return False, None
