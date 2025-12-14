#include <Arduino.h>
#include "ClockDisplayHAL.h"
#include "NetworkManager.h"
#include "SerialHelper.h"
#include "config.h"
#include "GifPlayer.h"
#include "WordClock.h"

NetworkManager networkManager(WIFI_SSID, WIFI_PASSWORD, GMT_OFFSET_SEC, DAYLIGHT_OFFSET_SEC);
ClockDisplayHAL clockDisplayHAL(LED_PIN, 255);
GifPlayer gifPlayer(&clockDisplayHAL);
WordClock wordClock(&clockDisplayHAL, &networkManager, &gifPlayer);
const bool TIME_DEBUG = true;

void setup()
{
  initSerial();
  networkManager.setup();
  clockDisplayHAL.setup();
  wordClock.setup();
}

void loop()
{
  if (TIME_DEBUG){
    for (uint16_t hour = 0; hour < 24; hour++)
    {
      for (uint16_t minute = 0; minute < 60; minute++)
      {
        wordClock.showTime(hour, minute, false);
        delay(60);
      }
    }
  }
  networkManager.update();
  wordClock.displayTime();
  delay(1000);
}
