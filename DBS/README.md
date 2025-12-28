# Dashboard Substystem (DBS) PC/Frontend
Frontend/web app, running on the PC or any device for remote operators to visualise data and interact with the system.
It interacts via HTTP with the Control Unit Subsystem.

---

The system is meant to monitor the rainwater level inside the tank, and -
depending on values - controlling the opening of a water channel connecting the tank to a network of water channers.

The overall system can be in two different modes: AUTOMATIC or MANUAL. 

In AUTOMATIC mode, the system automatically controls the opening of the water channel, depending on the current rainwater level in the tank.
In MANUAL mode, the opening is controlled manually by an operator. The starting mode when booting is AUTOMATIC.

---

The DBS subsystem is a dashboard for visualising the state of the Tank Monitoring system, including:
- A graph of the rainwater level, considering the last N measurements.
- The current value of the valve opening percentage.
- The state of the system: MANUAL, AUTOMATIC, UNCONNECTED or NOT AVAILABLE.
  - the state is labelled as NOT AVAILABLE when the CUS is not reachable, for any reason.

Besides, it includes:
- a GUI button to switch the modality (MANUAL, AUTOMATIC).
- a GUI widget to control the opening level of the valve in the WCS (when in MANUAL mode).
