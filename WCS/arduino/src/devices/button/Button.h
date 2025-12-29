#ifndef __BUTTON__
#define __BUTTON__

class Button {
    public:
        Button();
        virtual bool isPressed() = 0;
        virtual bool isClicked() = 0;

        // virtual void sync(); // TODO: controlla dove
        long getLastSynchTime(); // TODO: rivedere
    protected:
        void updateSyncTime(long time); // TODO
    private:
        long lastTimeSync; // TODO
};

#endif