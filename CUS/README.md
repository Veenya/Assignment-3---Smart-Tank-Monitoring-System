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