#include "Arduino.h"
#include "Valve.h"
#include "config.h"
#include "kernel/Logger.h"

bool DEBUGGING = true;

//TODO: Get info from CUS



Valve::Valve(HWPlatform* pHW) {
    this->pHW = pHW;
    //! Maybe get the state from TMS
    //! and other hardware
    this->tankMode = TankMode::AUTOMATIC;
    this->degrees = 0;
    this->waterLevel = getWaterLevel();
}

void Valve::init() {
    // We start off automatic
    automatic = true;

    //TankMode tankMode;
    //tankMode = TankMode::AUTOMATIC;
    // Check CUS info, based on that open the valve

    // The opening depends on the CUS system
    //WaterLevel waterLevel;
    //waterLevel = getWaterLevel();

    /*
    If button is pressed, we change mode...
    If we are in manual and we sense potentiometer change, 
    we change the degrees
    */

}

void Valve::sync() {}

/* ----------- Valve -----------*/

void setValveOpening(int degrees) {}

int getValveOpening() {}

/* --------------- Tank State Setters --------------*/

void Valve::setAutomatic() {
    this->automatic = true;
    this->manual = false;
    this->unconnected = false;
    this->not_available = false;
}

void Valve::setManual() {
    this->automatic = false;
    this->manual = true;
    this->unconnected = false;
    this->not_available = false;
}

void Valve::setUnconnected() {
    this->automatic = false;
    this->manual = false;
    this->unconnected = true;
    this->not_available = false;
}

void Valve::setNotAvailable() {
    this->automatic = false;
    this->manual = false;
    this->unconnected = false;
    this->not_available = true;
}