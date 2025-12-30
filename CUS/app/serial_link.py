# Made by ChatGPT

from __future__ import annotations
import threading
import time
from dataclasses import dataclass
from typing import Optional, Callable

import serial  # pyserial

from .state import SharedState, SystemMode


@dataclass
class SerialConfig:
    port: str = "COM3"       # change for your OS
    baud: int = 9600
    timeout: float = 0.2


class SerialLink:
    """
    Serial protocol (line-based):
      CUS -> WCS:
        SET:MODE:AUTO
        SET:MODE:MANUAL
        SET:OPEN:50
      WCS -> CUS:
        EVT:BTN
        STA:MODE:AUTO
        STA:OPEN:37
    """
    def __init__(self, cfg: SerialConfig, st: SharedState):
        self.cfg = cfg
        self.st = st
        self._ser: Optional[serial.Serial] = None
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None

        # external callback (optional)
        self.on_button_event: Optional[Callable[[], None]] = None

    def start(self) -> None:
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, name="SerialLink", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=1.0)
        self._close()

    def _open(self) -> None:
        try:
            self._ser = serial.Serial(self.cfg.port, self.cfg.baud, timeout=self.cfg.timeout)
            self.st.set_serial_connected(True)
        except Exception:
            self._ser = None
            self.st.set_serial_connected(False)

    def _close(self) -> None:
        try:
            if self._ser:
                self._ser.close()
        except Exception:
            pass
        self._ser = None
        self.st.set_serial_connected(False)

    def send_line(self, line: str) -> None:
        if not line.endswith("\n"):
            line = line + "\n"
        self.st.note_serial_tx(line.strip())

        if not self._ser or not self._ser.is_open:
            return
        try:
            self._ser.write(line.encode("utf-8"))
        except Exception:
            self._close()

    def send_mode_and_opening(self) -> None:
        snap = self.st.snapshot()
        mode = snap["mode"]
        opening = snap["desired_opening"]

        if mode == SystemMode.AUTOMATIC.value:
            self.send_line("SET:MODE:AUTO")
        elif mode == SystemMode.MANUAL.value:
            self.send_line("SET:MODE:MANUAL")
        elif mode == SystemMode.UNCONNECTED.value:
            # WCS should show UNCONNECTED; we can still force close
            self.send_line("SET:MODE:UNCONNECTED")
            self.send_line("SET:OPEN:0")
            return

        self.send_line(f"SET:OPEN:{opening}")

    def _handle_rx(self, line: str) -> None:
        self.st.note_serial_rx(line)

        # EVT:BTN => request toggle mode
        if line == "EVT:BTN":
            if self.on_button_event:
                self.on_button_event()
            return

        # STA:OPEN:xx
        if line.startswith("STA:OPEN:"):
            try:
                val = int(line.split(":")[2])
                self.st.set_actual_opening(val)
            except Exception:
                pass
            return

        # STA:MODE:MANUAL/AUTO
        if line.startswith("STA:MODE:"):
            m = line.split(":")[2].strip()
            if m == "AUTO":
                self.st.set_mode(SystemMode.AUTOMATIC)
            elif m == "MANUAL":
                self.st.set_mode(SystemMode.MANUAL)
            elif m == "UNCONNECTED":
                self.st.set_mode(SystemMode.UNCONNECTED)
            return

    def _run(self) -> None:
        while not self._stop.is_set():
            if self._ser is None:
                self._open()
                time.sleep(0.5)
                continue

            try:
                raw = self._ser.readline()
                if raw:
                    line = raw.decode("utf-8", errors="ignore").strip()
                    if line:
                        self._handle_rx(line)
            except Exception:
                self._close()
                time.sleep(0.5)
