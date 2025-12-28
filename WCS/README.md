# Water Channel Subsystem (WCS) - based on Arduino
Embedded system controlling the water channel connecting the tank with the water channel network.
It interacts via serial line with the Control Unit Subsystem (CUS).
It provides a panel for human operators to interact in place.

---

## Hardware components

### [TMS]
[
SoC ESP32 board (or ESP8266) including:
- 1 sonar
- 1 green led
- 1 red led
]

### WCS
Microcontroller Arduino UNO board including:
- 1 servo motor
- 1 potentiometer
- 1 tactile button
- 1 LCD display

---

The WCS subsystem is responsible for controlling a valve (with a motor) opening/closing a water channel draining water from the tank to the water channel network.

The opening range is in percentage: from 0% = channel closed (motor position 0 degree), up to 100% = channel full open (motor position 90° degree).
The water channel opening level depends on the state of the system, established by the CUS subsystem (see later).
The WCS includes a button to enable the MANUAL mode, in particular:
When the button is pressed, the system enters in MANUAL mode, so that the water channel opening level can be manually controlled by operators using a potentiometer.
To exit from the MANUAL model, the button must be pressed again.
The WCS subsystem is equipped also with an LCD display reporting:
the current valve opening level of the water channel.
the current mode (AUTOMATIC or MANUAL), or UNCONNECTED (see later).

---

About the WCS subsystem:
It must run on an Arduino (or an equivalent MCU board).
The control logic must be designed and implemented using finite state machines (synchronous or asynchronous) and (possibly, if useful) task-based architectures.
It must communicate with the CUS subsystem via serial line.