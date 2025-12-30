How to run it (CUS)

From inside cus/:

pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000


Open:

http://127.0.0.1:8000/status

http://127.0.0.1:8000/docs

What you MUST change

Set your Arduino serial port:

Windows: set WCS_PORT=COM4 (or use VS Code env / .env)

Linux: export WCS_PORT=/dev/ttyACM0

If you tell me your OS + the port name you see, I’ll give you the exact command.

If you want, next I can also generate a tiny DBS (index.html + app.js) that polls /status and lets you toggle mode + slider when MANUAL.








# CUS - Control Unit Subsystem
## Backend/Server

Parte centrale di tutto, comunica con tutti:
- con TMS con MQTT
- con WCS con sERIAL
- con DBS con HTTP

---

The CUS subsystem is in charge of the policy governing the behaviour of the system:
- Rainwater level monitoring
    - When rainwater level > L1 (and level < L2) [note: L1 < L2] for more than T1 time, then *the water channel is opened at 50%* until the level is < L1.
    - If level > L2 it is opened at 100%, until the level < L2

If the CUS is not receiving data for more than T2 time units from the TMS, then the system enters in `UNCONNECTED` state. It can go back to normal after communication is back.

---

L1
L2
T1
T3
F