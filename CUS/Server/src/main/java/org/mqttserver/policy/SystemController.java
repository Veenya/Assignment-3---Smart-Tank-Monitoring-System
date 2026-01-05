package org.mqttserver.policy;

import io.vertx.core.buffer.Buffer;
import org.mqttserver.presentation.Status;
import org.mqttserver.services.MQTT.Broker;

import java.util.Map;

public interface SystemController {

    void setWL(float wl); // Sets water level read from TMS (MQTT)

    Status getStatus();  // Returns the status
    float getWl();       // Returns water level

    int getValveValue(); // Returns valve value

    void setValveValueFromDashboard(int valveValue); // Manually sets value

    Map<Status, Integer> getStatusValveValue();  

    int getFrequency();

    void checkValveValue(String msg, Broker broker); // Checks arduino set the valve right

    void setIsManual(boolean isManual);   // Toggle Manual and Auto

    boolean getIsManual();
}
