#include <Arduino.h>
#include "model/HWPlatform.h"

HWPlatform hw;

void setup() {
  Serial.begin(9600);
  hw.init();
  hw.test();
}

void loop() {
  
}