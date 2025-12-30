/*
This is the central model. 
It stores the tank state and exposes simple actions (moving valve).
Then synch applies the current state to outputs (like states and LCD...).

IT needs to contain:
tankState (MANUAL, AUTOMATIC, UNDETECTED, NOT AVAILABLE)
valveOpen/valveState??? something like that

init()
- Resets flags and shit
- Turns motor on, closes valve...
- make state Automatic

valve control... Invent something idk


*/