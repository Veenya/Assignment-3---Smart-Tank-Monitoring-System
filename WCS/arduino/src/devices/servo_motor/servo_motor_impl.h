#ifndef __SERVO_MOTOR_IMPL__
#define __SERVO_MOTOR_IMPL__

#include "servo_motor.h"
#include <arduino.h>
#include "ServoTimer2.h"
// #include <Servo.h> //! non si può usare perché usa Timer1 che serve per l'interrupt dello scheduler

class ServoMotorImpl: public ServoMotor {
    public:
        ServoMotorImpl(int pin);
        void motorOn();
        bool isOn();
        void setPosition(int angle);
        void off();
        
    private:
        int pin; 
        bool _on;
        ServoTimer2 motor; 
};

#endif