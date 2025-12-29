#ifndef __BUTTON_IMPL__
#define __BUTTON_IMPL__

#include "Button.h"

class ButtonImpl: public Button {
    public:
        ButtonImpl(int pin);
        bool isPressed();
        bool isClicked();
        void sync();
    protected:
        int pin;
        bool pressed;
        bool clicked;
};

#endif