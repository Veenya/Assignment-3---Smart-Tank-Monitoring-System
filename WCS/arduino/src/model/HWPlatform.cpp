#include <Arduino.h>
#include "HWPlatform.h"

#include "devices/button/ButtonImpl.h"
#include "devices/servo_motor/servo_motor_impl.h"
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

HWPlatform::HWPlatform() {
    pValve = new ServoMotorImpl(SERVO_PIN);
    pLcd = new LiquidCrystal_I2C(LCD_ADDR, LCD_COLS, LCD_ROWS);
    pButton = new ButtonImpl(BUTTON_PIN);
    Serial.println("HWPlatform instantiated");
}

// --- Initialization ---

void HWPlatform::init() {
    pLcd->init(); // Default
    pLcd->backlight();
    Serial.println("HWPlatform initialized");
}

// --- Getters ---

ServoMotor* HWPlatform::getValve() {
    return this->pValve;
}

LiquidCrystal_I2C* HWPlatform::getLcd() {
    return this->pLcd;
}

ButtonImpl* HWPlatform::getButton() {
    return this->pButton;
}

// --- HW Test ---

void HWPlatform::test() {

}