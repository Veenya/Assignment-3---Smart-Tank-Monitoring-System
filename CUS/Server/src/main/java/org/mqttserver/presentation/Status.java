package org.mqttserver.presentation;

/**
 * This enum represents the statuses of the system*/
public enum Status {

    NORMAL,
    PRE_ALARM,
    ALARM,
    UNCONNECTED,
    INVALID_STATUS;


    @Override
    public String toString() {
        return switch (this) {
            case NORMAL -> "NORMAL";
            case PRE_ALARM -> "PRE-ALARM: WL TOO HIGH";
            case ALARM -> "ALARM: WL TOO HIGH";
            case UNCONNECTED -> "UNCONNECTED";
            case INVALID_STATUS -> "INVALID STATUS";
            default -> throw new IllegalArgumentException("Illegal status: " + this);
        };
    }
}
