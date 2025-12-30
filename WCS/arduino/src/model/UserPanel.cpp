#include "UserPanel.h"
#include "Arduino.h" //TODO: maybe remove
#include "config.h" //TODO: maybe remove

UserPanel::UserPanel(HWPlatform* pHW) {
    this->pHW = pHW;
    pButton = nullptr;
    pLcd = nullptr;
    buttonPressed = false; 
    prevButtonPressed = false; 

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

void UserPanel::turnOnDisplay(){
  pLcd->display();
  pLcd->clear();
}

void UserPanel::turnOffDisplay(){
  pLcd->noDisplay();
}

void UserPanel::displayManual() {
    pLcd->clear();
    pLcd->setCursor(0, 0); 
    pLcd->print("MANUAL");
}

void UserPanel::displayAutomatic() {
    pLcd->clear();
    pLcd->setCursor(0, 0); 
    pLcd->print("AUTOMATIC");
}

void UserPanel::displayUnconnected() {
    pLcd->clear();
    pLcd->setCursor(0, 0); 
    pLcd->print("UNCONNECTED");
}

void UserPanel::displayNotAvailable() {
    pLcd->clear();
    pLcd->setCursor(0, 0); 
    pLcd->print("NOT AVAILABLE");
}

void UserPanel::sync() {
  if (!pButton) {
    return;
  }
  prevButtonPressed = buttonPressed;
  buttonPressed = pButton->isPressed();
}

bool UserPanel::isButtonPressed() const {
  return buttonPressed; 
}

bool UserPanel::isButtonPressedEdge() {
  // fronte di salita: ora premuto, prima no
  return (buttonPressed && !prevButtonPressed);
}