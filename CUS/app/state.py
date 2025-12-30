# This was made by  ChatGPT   

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from threading import Lock
from time import time
from typing import Optional, Dict, Any


class SystemMode(str, Enum):
    AUTOMATIC = "AUTOMATIC"
    MANUAL = "MANUAL"
    UNCONNECTED = "UNCONNECTED"
    NOT_AVAILABLE = "NOT_AVAILABLE"   # usually means CUS down; kept for completeness


@dataclass
class SharedState:
    lock: Lock = field(default_factory=Lock, repr=False)

    # Latest tank level (0..100)
    tank_level: Optional[float] = None
    last_level_ts: Optional[float] = None  # epoch seconds

    # Mode
    mode: SystemMode = SystemMode.AUTOMATIC
    last_mode_change_ts: float = field(default_factory=time)

    # Valve opening percentage (0..100)
    desired_opening: int = 0     # what CUS wants WCS to set
    actual_opening: Optional[int] = None  # what WCS reports back (optional)

    # Connection health
    mqtt_connected: bool = False
    serial_connected: bool = False

    # For debugging / UI
    last_serial_rx: Optional[str] = None
    last_serial_tx: Optional[str] = None

    def snapshot(self) -> Dict[str, Any]:
        with self.lock:
            return {
                "mode": self.mode.value,
                "tank_level": self.tank_level,
                "last_level_ts": self.last_level_ts,
                "desired_opening": self.desired_opening,
                "actual_opening": self.actual_opening,
                "mqtt_connected": self.mqtt_connected,
                "serial_connected": self.serial_connected,
                "last_serial_rx": self.last_serial_rx,
                "last_serial_tx": self.last_serial_tx,
                "server_time": time(),
            }

    def set_mode(self, mode: SystemMode) -> None:
        with self.lock:
            self.mode = mode
            self.last_mode_change_ts = time()

    def set_desired_opening(self, opening: int) -> None:
        opening = max(0, min(100, int(opening)))
        with self.lock:
            self.desired_opening = opening

    def update_level(self, level: float) -> None:
        with self.lock:
            self.tank_level = float(level)
            self.last_level_ts = time()

    def set_actual_opening(self, opening: int) -> None:
        opening = max(0, min(100, int(opening)))
        with self.lock:
            self.actual_opening = opening

    def set_mqtt_connected(self, ok: bool) -> None:
        with self.lock:
            self.mqtt_connected = bool(ok)

    def set_serial_connected(self, ok: bool) -> None:
        with self.lock:
            self.serial_connected = bool(ok)

    def note_serial_rx(self, line: str) -> None:
        with self.lock:
            self.last_serial_rx = line

    def note_serial_tx(self, line: str) -> None:
        with self.lock:
            self.last_serial_tx = line
