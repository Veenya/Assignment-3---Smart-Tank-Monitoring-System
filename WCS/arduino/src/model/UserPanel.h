#ifndef __USER_PANEL__
#define __USER_PANEL__

#include "HWPlatform.h"

/*
 * Class for handling user interface. It deals with:
 * - LCD screen
 * - Button
*/

class UserPanel {
    public:
        // pHW is the hardware platform where we get the hw components
        UserPanel(HWPlatform* pHW);

        // Logic initialization
        // (internal states reset)
        void init();

        // --- LCD methods ---
        void turnOnDisplay();
        void turnOffDisplay();
        void displayManual();
        void displayAutomatic();
        void displayUnconnected();
        void displayNotAvailable();

        // sync() reads the physical state of the button\
        // and updates internal variables.
        // It needs to be called every task tick
        void sync();

        // Returns true if button is being pressed
        bool isButtonPressed() const;

        // Returns true only if the button goes from "not pressed" to "pressed"
        bool isButtonPressedEdge();
    private:
        HWPlatform* pHW;
        ButtonImpl* pButton;
        LiquidCrystal_I2C* pLcd;

        bool buttonPressed; // current state
        bool prevButtonPressed; // previous tick state

};

#endif