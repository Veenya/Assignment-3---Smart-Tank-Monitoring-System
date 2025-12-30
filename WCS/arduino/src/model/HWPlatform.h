#ifndef __HW_PLATFORM__
#define __HW_PLATFORM__

#include "config.h" // pins
#include "devices/button/ButtonImpl.h"
#include "devices/servo_motor/servo_motor_impl.h"
#include "devices/potentiometer/pot.h"
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

/*
 * Class for hardware handling. It deals with:
 * - Hardware components
 * - Testing Hardware
*/

class HWPlatform {
    public:
        HWPlatform();
        void init();
        void test();

        ServoMotor* getValve();
        LiquidCrystal_I2C* getLcd();
        ButtonImpl* getButton();
        Potentiometer* getPot();
    private:
        ServoMotor* pValve;
        LiquidCrystal_I2C* pLcd;
        ButtonImpl* pButton;
        Potentiometer* pPot;
};

#endif