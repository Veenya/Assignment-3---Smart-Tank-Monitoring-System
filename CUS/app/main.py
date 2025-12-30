from __future__ import annotations
import os
import threading
import time
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .state import SharedState, SystemMode
from .policy import Policy, PolicyConfig
from .mqtt_client import MqttClient, MqttConfig
from .serial_link import SerialLink, SerialConfig

app = FastAPI(title="CUS - Smart Tank Monitoring System")

# Allow browser dashboard (DBS) to call the API easily
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for assignment/dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

st = SharedState()

# Config from environment (so you don't hardcode ports)
policy_cfg = PolicyConfig(
    L1=float(os.getenv("CUS_L1", "60")),
    L2=float(os.getenv("CUS_L2", "85")),
    T1=float(os.getenv("CUS_T1", "5")),
    T2=float(os.getenv("CUS_T2", "10")),
)

mqtt_cfg = MqttConfig(
    host=os.getenv("MQTT_HOST", "localhost"),
    port=int(os.getenv("MQTT_PORT", "1883")),
    topic_level=os.getenv("MQTT_TOPIC_LEVEL", "tank/level"),
)

serial_cfg = SerialConfig(
    port=os.getenv("WCS_PORT", "COM3"),
    baud=int(os.getenv("WCS_BAUD", "9600")),
)

policy = Policy(policy_cfg)
mqttc = MqttClient(mqtt_cfg, st)
serlink = SerialLink(serial_cfg, st)

# background policy loop
_stop_policy = threading.Event()
_policy_thread: Optional[threading.Thread] = None


def toggle_mode():
    # Toggle AUTO <-> MANUAL; if UNCONNECTED, keep UNCONNECTED unless data resumes
    if st.mode == SystemMode.AUTOMATIC:
        st.set_mode(SystemMode.MANUAL)
    elif st.mode == SystemMode.MANUAL:
        st.set_mode(SystemMode.AUTOMATIC)


def _policy_loop():
    # Runs policy at ~10Hz and pushes changes to WCS
    while not _stop_policy.is_set():
        should_send, _reason = policy.tick(st)
        if should_send:
            serlink.send_mode_and_opening()
        time.sleep(0.1)


serlink.on_button_event = lambda: (toggle_mode(), serlink.send_mode_and_opening())


@app.on_event("startup")
def on_startup():
    global _policy_thread
    mqttc.start()
    serlink.start()

    _stop_policy.clear()
    _policy_thread = threading.Thread(target=_policy_loop, name="PolicyLoop", daemon=True)
    _policy_thread.start()


@app.on_event("shutdown")
def on_shutdown():
    _stop_policy.set()
    try:
        mqttc.stop()
    except Exception:
        pass
    try:
        serlink.stop()
    except Exception:
        pass


class ModeReq(BaseModel):
    mode: SystemMode


class OpeningReq(BaseModel):
    opening: int  # 0..100


@app.get("/status")
def get_status():
    return st.snapshot()


@app.post("/mode")
def set_mode(req: ModeReq):
    # allow switching between AUTO and MANUAL via dashboard
    if req.mode not in (SystemMode.AUTOMATIC, SystemMode.MANUAL):
        raise HTTPException(status_code=400, detail="Mode must be AUTOMATIC or MANUAL")
    st.set_mode(req.mode)
    serlink.send_mode_and_opening()
    return st.snapshot()


@app.post("/opening")
def set_opening(req: OpeningReq):
    # only makes sense in MANUAL
    if st.mode != SystemMode.MANUAL:
        raise HTTPException(status_code=409, detail="Can set opening only in MANUAL mode")
    st.set_desired_opening(req.opening)
    serlink.send_mode_and_opening()
    return st.snapshot()
