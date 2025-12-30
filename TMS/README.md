1) TMS (ESP32) — water-level-monitoring-subsystem/src/main.cpp

Qui vedi esattamente cosa deve fare il TMS:

legge il sonar (Sonar sonar = Sonar(...))

pubblica su MQTT il livello ogni tot millisecondi (variabile frequency)

accende LED verde/rosso in base a connessione WiFi/MQTT

usa FreeRTOS con 3 task:

TaskPublisher: pubblica water level su topic

TaskSubscriber: ascolta un topic per cambiare frequency

TaskCheckConnection: se WiFi/MQTT cade, prova a riconnettere

📌 I topic e i campi JSON sono in src/env/config.h/.cpp:

wl_topic = "/sensor/wl"

payload JSON contiene campo "WL" (water level)

👉 Per il tuo progetto: stessa cosa, solo che il valore è “tank level”.