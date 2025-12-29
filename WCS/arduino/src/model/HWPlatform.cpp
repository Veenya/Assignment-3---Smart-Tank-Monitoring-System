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
    Serial.println(F("[HW TEST] Starting..."));

    // --- LCD test ---
    if (pLcd) {
        pLcd->clear();
        pLcd->setCursor(0, 0);
        pLcd->print("HW TEST");
        pLcd->setCursor(0, 1);
        pLcd->print("LCD OK");
        Serial.println(F("[HW TEST] LCD OK"));
    } else {
        Serial.println(F("[HW TEST] ERROR: LCD is null"));
    }

    // --- Button test ---
    if (pButton) {
        Serial.println(F("[HW TEST] Button test: press button within 5s..."));
        if (pLcd) {
            pLcd->setCursor(0, 2);
            pLcd->print("Press button...");
        }
        unsigned long start = millis();
        bool pressedOnce = false;

        while (millis()- start<5000) {
            pButton->sync();
            if (pButton->isPressed()) {
                pressedOnce = true;
                Serial.println(F("[HW TEST] Button PRESSED"));
                if (pLcd) {
                    pLcd->setCursor(0, 3);
                    pLcd->print("Button OK        "); // TODO: find a way to make it work without Padding
                }
                delay(300); // Debounce
            }
            delay(10);
        }
        if (!pressedOnce) {
            Serial.println(F("[HW TEST] Button NOT pressed"));
            if (pLcd) {
                pLcd->setCursor(0, 3);
                pLcd->print("No press seen    "); // TODO: find a way to make it work without Padding
            }
        }
    } else {
        Serial.println(F("[HW TEST] ERROR: Button is null"));
    }

    // --- Servo test ---
    if (pValve) {
        Serial.println(F("[HW TEST] Servo test..."));
        if (pLcd) {
            pLcd->clear();
            pLcd->setCursor(0, 0);
            pLcd->print("SERVO TEST");
        }
        pValve->motorOn();    //! Not sure what this does but ok
        Serial.println(F("[HW TEST] Servo ON"));

        // Move to 0 degrees
        if (pLcd) {
            pLcd->setCursor(0, 1);
            pLcd->print("Pos: 0   ");
        }
        Serial.println(F("[HW TEST] Servo -> 0"));
        pValve->setPosition(0);
        delay(1000);

        // Move to 90 degrees
        if (pLcd) {
            pLcd->setCursor(0, 1);
            pLcd->print("Pos: 90  ");
        }
        Serial.println(F("[HW TEST] Servo -> 90"));
        pValve->setPosition(90);
        delay(1000);

        // Move to 180 degrees
        if (pLcd) {
            pLcd->setCursor(0, 1);
            pLcd->print("Pos: 180  ");
        }
        Serial.println(F("[HW TEST] Servo -> 180"));
        pValve->setPosition(180);
        delay(1000);

        // Move Back to 90 degrees
        if (pLcd) {
            pLcd->setCursor(0, 1);
            pLcd->print("Pos: 90  ");
        }
        Serial.println(F("[HW TEST] Servo -> 90 (neutral)"));
        pValve->setPosition(90);
        delay(1000);

        pValve->off();
        Serial.println(F("[HW TEST] Servo OFF"));

        if (pLcd) {
            pLcd->setCursor(0, 2);
            pLcd->print("SERVO OK");
            pLcd->setCursor(0, 3);
            pLcd->print("DONE");
        }
    } else {
        Serial.println(F("[HW TEST] ERROR: Servo is null"));
        if (pLcd) {
            pLcd->clear();
            pLcd->setCursor(0, 0);
            pLcd->print("HW TEST FAIL");
            pLcd->setCursor(0, 1);
            pLcd->print("Servo null");
        }
    }
    Serial.println(F("[HW TEST] Completed."));
}