from __future__ import annotations
import threading
import time
from dataclasses import dataclass
from typing import Optional

import paho.mqtt.client as mqtt

from .state import SharedState


@dataclass
class MqttConfig:
    host: str = "localhost"
    port: int = 1883
    topic_level: str = "tank/level"   # TMS publishes here
    client_id: str = "cus"
    keepalive: int = 30


class MqttClient:
    def __init__(self, cfg: MqttConfig, st: SharedState):
        self.cfg = cfg
        self.st = st
        self._client = mqtt.Client(client_id=self.cfg.client_id, clean_session=True)
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_message = self._on_message

        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, name="MqttClient", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        try:
            self._client.loop_stop()
        except Exception:
            pass
        try:
            self._client.disconnect()
        except Exception:
            pass
        if self._thread:
            self._thread.join(timeout=1.0)

    def _on_connect(self, client, userdata, flags, rc):
        ok = (rc == 0)
        self.st.set_mqtt_connected(ok)
        if ok:
            client.subscribe(self.cfg.topic_level)

    def _on_disconnect(self, client, userdata, rc):
        self.st.set_mqtt_connected(False)

    def _on_message(self, client, userdata, msg):
        # Expect payload like "72" (percent) or "72.5"
        try:
            payload = msg.payload.decode("utf-8", errors="ignore").strip()
            level = float(payload)
            # clamp
            if level < 0:
                level = 0.0
            if level > 100:
                level = 100.0
            self.st.update_level(level)
        except Exception:
            # ignore malformed messages
            pass

    def _run(self) -> None:
        # reconnect loop
        while not self._stop.is_set():
            try:
                self._client.connect(self.cfg.host, self.cfg.port, keepalive=self.cfg.keepalive)
                self._client.loop_start()

                while not self._stop.is_set():
                    time.sleep(0.2)

                return
            except Exception:
                self.st.set_mqtt_connected(False)
                time.sleep(1.0)
