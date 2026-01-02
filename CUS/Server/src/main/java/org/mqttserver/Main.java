package main.java.org.mqttserver;

// Vert.x runtime used to run the HTTP server "verticle"
//? What?
import io.vertx.core.Vertx;
// Manages talking to Arduino with Serial
// TODO: do? Do the doing...
import org.mqttserver.policy.ChannelControllerManager;
import org.mqttserver.policy.ChannelControllerManagerImpl;
// Enum representing the system status.
import org.mqttserver.presentation.Status;
// The HTTP API service (GET system data, POST commands from dashboard)
import org.mqttserver.services.HTTP.DataService;
// MQTT srever/broker
import org.mqttserver.services.MQTT.Broker;
import org.mqttserver.services.MQTT.BrokerImpl;

public class Main {
    public static void main(String[] args) throws Exception {
        // TODO: change
        System.out.println("Welcome in Smart River Monitoring Server...");
        // Creates MQTT broker object
        Broker broker = new BrokerImpl();
        broker.initialize(broker.getMqttServer());

        //start the httpServer and DataService (for dashboard and http server)
        Vertx vertx = Vertx.vertx();
        DataService service = new DataService(8050, broker);
        vertx.deployVerticle(service);

        //Init Channel Controller Manager
        ChannelControllerManager channelControllerManager = new ChannelControllerManagerImpl(broker);

        while (true) {
            if (!broker.getSystemController().getIsManual()) {
                channelControllerManager.sendMessageToArduino(Status.ALARM_TOO_HIGH); //I send the message to arduino with state
                String msg = channelControllerManager.receiveDataFromArduino(); //I receive the answer from arduino
                broker.getSystemController().checkValveValue(msg, broker); //check valve value
            } else {
                channelControllerManager.sendMessageToArduino(broker.getSystemController().getValveValue()); //I send the message to arduino with state
            }
            Thread.sleep(400);
        }
    }
}