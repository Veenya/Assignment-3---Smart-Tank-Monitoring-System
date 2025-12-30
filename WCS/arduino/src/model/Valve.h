#ifndef __VALVE__
#define __VALVE__

#include "States.h"
#include "config.h"
#include "HWPlatform.h"

class Valve {
    public:
        Valve(HWPlatform* hw);
        void init();
        void sync();

        // ------------- Tank Mode ------------
        TankMode getTankMode();

        // ------------- Valve opening ------------
        void setValveOpening(int degree);
        int getValveOpening(); // Potentiometer

        //TODO: Use WaterLevel somehow
        //! Needs to comunicate with the water sensor
        WaterLevel getWaterLevel();

        void setAutomatic();
        void setManual();
        void setUnconnected();
        void setNotAvailable();

    private:
        HWPlatform* pHW;
        TankMode tankMode;
        WaterLevel waterLevel; //!
        int degrees;

        // States
        // MANUAL, AUTOMATIC, UNCONNECTED, NOT_AVAILABLE
        bool automatic;
        bool manual;
        bool unconnected;
        bool not_available;
};

#endif