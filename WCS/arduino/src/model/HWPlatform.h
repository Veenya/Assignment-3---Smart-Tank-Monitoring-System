#ifndef __HW_PLATFORM__
#define __HW_PLATFORM__

#include "config.h" // pins
#include "devices/button/ButtonImpl.h"
#include "devices/servo_motor/servo_motor_impl.h"
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

class HWPlatform {
    public:
        HWPlatform();
        void init();
        voit test();

        ServoMotor* getValve();
        LiquidCrystal_I2C* getLcd();
        ButtonImpl* getButton();
    private:
        ServoMotor* pValve;
        LiquidCrystal_I2C pLcd;
        ButtonImpl* pButton;
};

#endif