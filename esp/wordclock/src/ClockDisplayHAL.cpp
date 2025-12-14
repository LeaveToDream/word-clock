#include "ClockDisplayHAL.h"

const uint32_t RAINBOW_COLORS[] = {
    0xF60000,
    0xFB6F01,
    0xFFEE00,
    0x4DE94C,
    0x3783FF,
    0x4815AA,
    0xC132AB};

ClockDisplayHAL::WordMapping const ClockDisplayHAL::WORDS_TO_LEDS[] = {
    {"DEMI", 19, 22},
    {"QUART", 25, 29},
    {"CINQ", 0, 3},
    {"DIX", 13, 15},
    {"VINGT", 7, 11},
    {"ET", 31, 32},
    {"LE", 32, 33},
    {"MOINS", 43, 47},
    {"PILE", 32, 35},
    {"HEURE", 36, 40},
    {"HEURES", 36, 41},
    {"HEURE_1", 61, 63},
    {"HEURE_2", 74, 77},
    {"HEURE_3", 84, 88},
    {"HEURE_4", 101, 106},
    {"HEURE_5", 92, 95},
    {"HEURE_6", 89, 91},
    {"HEURE_7", 79, 82},
    {"HEURE_8", 49, 52},
    {"HEURE_9", 96, 99},
    {"HEURE_10", 117, 119},
    {"HEURE_11", 54, 57},
    {"MIDI", 120, 123},
    {"MINUIT", 65, 70},
    {"EST", 126, 128},
    {"IL", 130, 131},
    {"BEST", 108, 111},
    {"MUM", 113, 115},
    {"KLV", 4, 6}
};

ClockDisplayHAL::ClockDisplayHAL(uint8_t pin, uint8_t brightness)
    : pixels(NUM_LEDS, pin, NEO_GRB + NEO_KHZ800), brightness(brightness)
{
}

void ClockDisplayHAL::setup()
{
    pixels.setBrightness(255);
    pixels.begin();
    pixels.show();
}

void ClockDisplayHAL::displayWord(const String &word, uint32_t color)
{
    for (auto mapping : WORDS_TO_LEDS)
    {
        if (word.equals(mapping.word))
        {
            for (uint8_t i = mapping.start; i <= mapping.end; ++i)
            {
                pixels.setPixelColor(i, color);
            }
            break;
        }
    }
}

void ClockDisplayHAL::playRainbow(unsigned long durationMs)
{
    unsigned long startTime = millis();
    unsigned long frequency = 300;
    unsigned long lastSecond = (millis() - startTime) / frequency;

    while (millis() - startTime < durationMs)
    {
        unsigned long second = (millis() - startTime) / frequency; 
        if (second != lastSecond) {
            lastSecond = second;
            for (uint16_t i = 108; i <= 111; i++)
            {
                uint32_t color = RAINBOW_COLORS[((115-i) + second) % 7];

                pixels.setPixelColor(i, color);
            }
            for (uint16_t i = 113; i <= 115; i++)
            {
                uint32_t color = RAINBOW_COLORS[((115-i) + second) % 7];

                pixels.setPixelColor(i, color);
            }
            for (uint16_t i = 4; i <= 6; i++)
            {
                uint32_t color = RAINBOW_COLORS[(i + second) % 7];

                pixels.setPixelColor(i, color);
            }
            pixels.show();
        }
        pixels.clear();
    }
}

uint16_t ClockDisplayHAL::cartesianToWordClockLEDStripIndex(uint8_t x, uint8_t y)
{
    uint16_t row_index;
    uint16_t index;

    if (y % 2 == 0)
    {
        row_index = NUM_LEDS - (y * WIDTH);
        index = row_index - (x + 1);
    }
    else
    {
        row_index = NUM_LEDS - ((y + 1) * WIDTH);
        index = row_index + x;
    }

    if (index < 0 || index >= NUM_LEDS)
    {
        return 0;
    }

    return index;
}

void ClockDisplayHAL::setPixel(uint8_t x, uint8_t y, uint32_t color)
{
    uint16_t index = cartesianToWordClockLEDStripIndex(x, y);
    pixels.setPixelColor(index, color);
}

void ClockDisplayHAL::clearPixels(bool show)
{
    pixels.clear();
    if (show)
    {
        pixels.show();
    }
}

void ClockDisplayHAL::show()
{
    pixels.show();
}