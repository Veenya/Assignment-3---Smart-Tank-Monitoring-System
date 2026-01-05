# Control Unit Subsystem (CUS)
This is the main subsystem, it coordinates the whole system.
It's the intermediary between all the system components.

The Backend Dashboard (CUS) communicates with:
- Arduino (WCS) using Serial Line 
- ESP32 (TMS) using MQTT 
- Frontend Dashboard (DBS) using HTTP 

---

## How to run CUS

1) (MQTT broker + HTTP API)

Windows:
```bash
cd CUS\Server
.\gradlew.bat run
```

Linux/macOS:
```bash
cd CUS/Server
chmod +x gradlew
./gradlew run
```

---

## What does the Control Unit (CUS) do?
The CUS subsystem is in charge of the policy governing the behaviour of the system. 
In particular it monitors the Rainwater Level:
 - When the rainwater level exceeds the level L1 (but below L2, with L1 < L2) for more than T1 time, the water channel is opened at 50% until the rainwater level is below L1.
 - If the the rainwater level exceeds the level L2, the water channel is immediately opened at 100%, until the value is below L2.

If the CUS is not receiving data for more than T2 time units from the TMS (because of network problems), then the system enters into an UNCONNECTED state, which is restored to a normal state only if/when the network problems are solved.

---

### Connection with HTTP (DBS)

The file used for this connection is ./src/services/HTTP/Dataservice.java

In the `start()` method we create the HTTP server.
The exposed APIs are:
 - `POST`: sets `valveValue`, and puts the system in `MANUAL`
 - `GET`: returns `status`, `valveValue`, `wl`

This function is called by `./Server/Main.java`

### Connection with MQTT (TMS)
TODO: Write paragraph...

### Connection with Serial (WCS)

We have three parts:
1) Port scanner
2) Serial channel
3) Who uses it