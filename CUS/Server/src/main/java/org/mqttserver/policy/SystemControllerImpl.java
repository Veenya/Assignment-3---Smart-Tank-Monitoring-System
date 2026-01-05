package org.mqttserver.policy;

import io.vertx.core.buffer.Buffer;
import org.mqttserver.presentation.JSONUtils;
import org.mqttserver.presentation.MessageFromArduino;
import org.mqttserver.presentation.MessageToArduino;
import org.mqttserver.presentation.Status;
import org.mqttserver.services.MQTT.Broker;

import java.util.HashMap;
import java.util.Map;


// TODO: Put new policy to determin state based on water level, valve percentage, and frequencies
//! This file is very important, careful!
public class SystemControllerImpl implements SystemController {

    private final double L1 = 5;  //? For our project we only
    private final double L2 = 20; //? need these two

    private final double INVALID_WL = -1; 
    // Frequenze associate agli stati
    private final int T0 = 0;
    private final int T1 = 6000; //1800ms
    private final int T2 = 12000;

    private Status status = null;
    private int valveValue = 0;
    private float wl = 0;
    private boolean isManual = false;
    private int frequency = 1;
    private final int V0= 0;
    private final int V1= 50;
    private final int V2 = 100;

    private long lastWlRxTimeMs = System.currentTimeMillis(); // ultimo wl ricevuto
    private Long betweenStartMs = null; // quando wl è entrato in (L1, L2)

    // TODO: Redo...
    private final Map<Status, Integer> statusValveValue = new HashMap<Status, Integer>() {{
        put(Status.NORMAL, V0);
        put(Status.PRE_ALARM, V1);
        put(Status.ALARM, V2);
    }};
    // TODO: Redo...
    private final Map<Status, Integer> statusFreq = new HashMap<Status, Integer>() {{
        put(Status.NORMAL, T0);
        put(Status.PRE_ALARM, T1);
        put(Status.ALARM, T0);
        put(Status.UNCONNECTED, T2);
        put(Status.INVALID_STATUS, T0);
    }};


    public SystemControllerImpl() {

    }

    /*
    setWL(wl)

    Quando arriva un valore di livello acqua:
        1) Stampa il valore
        2) Se non e' valido (wl > -1)
            - salva this.wl = wl
            - calcola this.status con gli if/else sulle soglie
            - calcola this.frequency = statusFreq.get(status)
        3) Se invalido -> status = INVALID_STATUS
        4) Stampa lo stato
    */

    @Override
    public void setWL(float wl) {
        long now = System.currentTimeMillis();
        // Arriva un dato => aggiorna "ultimo dato ricevuto"
        lastWlRxTimeMs = now;

        // Prints current water level
        System.out.println("WL RECEIVED VALUE: " + wl);

        // Se era UNCONNECTED e ora arrivano dati, torna operativo
        if (this.status == Status.UNCONNECTED) {
            betweenStartMs = null; // Reset timer 
        }
        
        if (wl > INVALID_WL) {
            // Set water level
            this.wl = wl;

            // PRIORITÀ 1: wl > L2 => valvola 100% immediata finché wl torna sotto/su L2
            if (wl > L2) {
                this.status = Status.ALARM;
                this.valveValue = 100;
                betweenStartMs = null; // Reset T1
                System.out.println("SET SYSTEM STATUS: " + this.status.toString().toUpperCase());
                //return;
            } else if (wl > L1) {
                if (betweenStartMs == null) {
                    betweenStartMs = now;
                }
                if (now - betweenStartMs >= T1) {
                    this.status = Status.PRE_ALARM;
                    this.valveValue = 50;
                } else {
                    this.status = Status.NORMAL;
                    this.valveValue = 0;
                }

            }
        } else {
            this.status = Status.INVALID_STATUS;
        }
        System.out.println("SET SYSTEM STATUS: " + this.status.toString().toUpperCase());
    }

    public void tickConnection() {
        long now = System.currentTimeMillis();
        if (now - lastWlRxTimeMs > T2) {
            this.status = Status.UNCONNECTED;
            this.valveValue = 0;      // scelta safe
            this.betweenStartMs = null;
        }
    }


    public Status getStatus() {
        if (this.status == null) {
            System.err.println("SERVER: STATUS undefined, check your connection to sensor");
            return null;
        }
        return this.status;
    }

    public Map<Status, Integer> getStatusValveValue() {
        return this.statusValveValue;
    }

    @Override
    public int getFrequency() {
        return this.frequency;
    }

    @Override
    public float getWl() {
        return this.wl;
    }

    @Override
    public int getValveValue() {
        return this.valveValue;
    }

    @Override
    public void setValveValueFromDashboard(int valveValue) {
        this.valveValue = valveValue;
    }

    /*
    chekcValveValue(msg, broker)

    Serve per "verificare" Arduino:
        - legge il JSON arrivato da Arduino (MessageFromArduino)
        - estrare valveValue
        - confronta con il valore atteso per lo stato corrente
            (expected = statusValveValue.get(currentStatus))
        - se uguale: ok e aggiorna this.value
        - se diverso: stampa errore
    */
    @Override
    public void checkValveValue(String msg, Broker broker) {
        try {
            System.out.println("ARDUINO SENT: " + msg);
            Integer valveValue = JSONUtils.jsonToObject(msg, MessageFromArduino.class).getValveValue();
            if (valveValue.equals(broker.getSystemController().getStatusValveValue().get(broker.getSystemController().getStatus()))) {
                System.out.println("SERVER: Valve value ok");
                this.valveValue = valveValue;
            } else {
                System.err.println("SERVER: Valve value incorrect for system state");
            }
        } catch (Exception ex) {
            System.err.println("Il server è In attesa di dati validi da parte di Arduino....");
        }
    }

    @Override
    public boolean getIsManual() {
        return this.isManual;
    }

    @Override
    public void setIsManual(boolean isManual) {
        this.isManual = isManual;
    }


}
