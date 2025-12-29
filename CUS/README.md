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