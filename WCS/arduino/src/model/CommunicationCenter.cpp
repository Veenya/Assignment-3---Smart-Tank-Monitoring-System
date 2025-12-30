#include "CommunicationCenter.h"
#include "kernel/MsgService.h"
#include "kernel/Logger.h"
#include "Arduino.h"

CommunicationCenter::CommunicationCenter(HWPlatform* pHW, Valve* pValve) : pHW(pHW), pValve(pValve) {
}

void CommunicationCenter::init() {
    this->pHW = pHW;
    this->pValve = pValve;
    this->degrees = 0;
    this->buttonPressed = false;
    this->currentTankMode = TankMode::AUTOMATIC;
    this->currentWaterLevel = WaterLevel::NORMAL; 
}

// ! wtf is this shit
bool CommunicationCenter::notifyButtonPressed() {
    // The state toggles... 
    // See it was pressed, then
    // change the tank mode (toggle manual and auto)
    // Send message to CUS

    this->currentTankMode = this->pValve->getTankMode(); //! Should we get it from here or make another file like Tank ???
    String tankStateStr;
    if (currentTankMode == TankMode::AUTOMATIC) {
        tankStateStr = "AUTO";
    } else if (currentTankMode == TankMode::MANUAL) {
        tankStateStr = "MANUAL";
    } else if (currentTankMode == TankMode::UNCONNECTED) {
        tankStateStr = "UNCONNECTED";
    } else if (currentTankMode == TankMode::NOT_AVAILABLE) {
        tankStateStr = "NOT_AVAILABLE"; //! TODO: Check again the behaviour
    } else {
        tankStateStr = "UNKNOWN";
    }
}

int CommunicationCenter::notifyValveOpeningChanged(int degrees) {
    this->degrees = degrees;
    return this->degrees;
}

// TODO: this
void CommunicationCenter::sync() {}