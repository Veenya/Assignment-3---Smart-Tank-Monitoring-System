#include "UserPanel.h"
#include "Arduino.h" //TODO: maybe remove?
#include "config.h" //TODO: maybe remove?

UserPanel::UserPanel(HWPlatform* pHW) {
    this->pHW = pHW;
    pButton = nullptr;
    pLcd = nullptr;
    buttonPressed = false; //! maybe remove?
    prevButtonPressed = false; //! maybe remove?

    if (pHW) {
        pButton = pHW->getButton();
        pLcd = pHW->getLcd();
    }
}

void UserPanel::init() {
  buttonPressed = false;
  prevButtonPressed = false;
  pLcd->init();
  pLcd->backlight();
  pLcd->noDisplay();
  turnOnDisplay();
}