#ifndef __COMMUNICATION_CENTER__
#define __COMMUNICATION_CENTER__

#include "config.h"
#include "HWPlatform.h"
#include "Valve.h"

/*
 * Classe che comunica con il con il CUS (Central Unit Subsystem) sul PC.
 * - Riceve comandi testuali via seriale (AUTO, MANUAL, OPEN).
 * - Espone metodi per i Task.
 * - Invia periodicamente lo stato corrente.

     CUS → WCS
    SET:MODE:AUTO\n
    SET:MODE:MANUAL\n
    SET:OPEN:50\n (0–100)
    WCS → CUS
    EVT:BTN\n (operator pressed local button)
    STA:MODE:AUTO\n (optional status)
    STA:OPEN:37\n (optional status)

 */

class CommunicationCenter {
    public:
        CommunicationCenter(HWPlatform* pHW, Valve* pValve); //! Do you need HWPlatform? or just Valve???
        void init();
        void sync();

        bool notifyButtonPressed(); // To change mode
        int notifyValveOpeningChanged(int degrees); // From potentiometer

    private:
        HWPlatform* pHW;
        Valve* pValve;

        int degrees;
        bool buttonPressed; // Maybe remove
        TankMode currentTankMode;
        WaterLevel currentWaterLevel; //! Find new name

        //unsigned long lastSendTime = 0;
        //const unsigned long sendInterval = 5000;
};

#endif