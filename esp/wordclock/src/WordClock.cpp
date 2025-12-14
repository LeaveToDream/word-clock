#include "WordClock.h"
#include "SerialHelper.h"

const uint32_t COLORS[] = {
    0xFF0000,
    0x00FF00,
    0x0000FF,
    0xFFFF00,
    0xFF00FF,
    0x00FFFF,
    0xFFFFFF,
    0xA52A2A};

WordClock::WordClock(ClockDisplayHAL *clockDisplayHAL, NetworkManager *networkManager, GifPlayer *gifPlayer)
    : clockDisplayHAL(clockDisplayHAL), networkManager(networkManager), gifPlayer(gifPlayer), lastHour(-1), allLastHighlightedWords(""), gifDownloaded(false) {}

void WordClock::setup()
{
    downloadGIF();
}

void WordClock::downloadGIF()
{
    if (!gifDownloaded)
    {
        const char *gifUrl = "https://raw.githubusercontent.com/johniak/word-clock/refs/heads/main/raspberry-pi/heart_art_small.gif";
        if (networkManager->downloadGIF(gifUrl))
        {
            uint8_t *gifBuffer = networkManager->getGifBuffer();
            size_t gifSize = networkManager->getGifBufferSize();
            if (gifSize > 0 && gifBuffer != nullptr)
            {
                if (gifPlayer->loadGIF(gifBuffer, gifSize))
                {
                    gifDownloaded = true;
                    SERIAL_PRINTLN("GIF downloaded and loaded successfully.");
                }
            }
        }
        else
        {
            SERIAL_PRINTLN("Failed to download GIF.");
        }
    }
}

void WordClock::highlightWord(const String &word, uint32_t color)
{
    clockDisplayHAL->displayWord(word, color);
}

uint32_t WordClock::getRandomColor()
{
    int index = random(0, sizeof(COLORS) / sizeof(COLORS[0]));
    return COLORS[index];
}



void WordClock::displayTime()
{
    struct tm currentTime = networkManager->getLocalTimeStruct();
    int hour = currentTime.tm_hour;
    int minute = currentTime.tm_min;

    showTime(hour, minute, true);
}

void WordClock::showTime(int hour, int minute, bool showRainbow)
{
    clockDisplayHAL->clearPixels(false);

    if (hour != lastHour && minute == 0 && showRainbow)
    {
        lastHour = hour;
        clockDisplayHAL->playRainbow(5000);
        if (gifDownloaded)
        {
            gifPlayer->playGIF(5000);
        }
        clockDisplayHAL->clearPixels(false);
    }

    highlightWord("IL", getRandomColor());
    highlightWord("EST", getRandomColor());
    String allHighlightedWords = "ILEST";

    // Handle hours
    if (minute >= 35)
    {
        hour = hour + 1;
    }
    if (hour==0 || hour==24) {
        highlightWord("MINUIT", getRandomColor());
        allHighlightedWords += "MINUIT";
    } else if (hour==12) {
        highlightWord("MIDI", getRandomColor());
        allHighlightedWords += "MIDI";
    } else {
        
        hour = hour % 12;

        String hourWord = "HEURE_" + String(hour);
        highlightWord(hourWord, getRandomColor());
        allHighlightedWords += hourWord;

        String h = (hour != 1) ? "HEURES" : "HEURE";
        highlightWord(h, getRandomColor());
        allHighlightedWords += h;
    }

    // Handle minutes
    if (minute < 5) {
        highlightWord("PILE", getRandomColor());
        allHighlightedWords += "PILE";
    } else if (minute < 10) {
        highlightWord("CINQ", getRandomColor());
        allHighlightedWords += "CINQ";
    } else if (minute < 15) {
        highlightWord("DIX", getRandomColor());
        allHighlightedWords += "DIX";
    } else if (minute < 20) {
        highlightWord("ET", getRandomColor());
        highlightWord("QUART", getRandomColor());
        allHighlightedWords += "ETQUART";
    } else if (minute < 25) {
        highlightWord("VINGT", getRandomColor());
        allHighlightedWords += "VINGT";
    } else if (minute < 30) {
        highlightWord("VINGT", getRandomColor());
        highlightWord("CINQ", getRandomColor());
        allHighlightedWords += "VINGTCINQ";
    }
    else if (minute < 35)
    {
        highlightWord("ET", getRandomColor());
        highlightWord("DEMI", getRandomColor());
        allHighlightedWords += "ETDEMI";
    }
    else if (minute < 40)
    {
        highlightWord("MOINS", getRandomColor());
        highlightWord("VINGT", getRandomColor());
        highlightWord("CINQ", getRandomColor());
        allHighlightedWords += "MOINSVINGTCINQ";
    }
    else if (minute < 45)
    {
        highlightWord("MOINS", getRandomColor());
        highlightWord("VINGT", getRandomColor());
        allHighlightedWords += "MOINSVINGT";
    }
    else if (minute < 50)
    {
        highlightWord("MOINS", getRandomColor());
        highlightWord("LE", getRandomColor());
        highlightWord("QUART", getRandomColor());
        allHighlightedWords += "MOINSLEQUART";
    }
    else if (minute < 55)
    {
        highlightWord("MOINS", getRandomColor());
        highlightWord("DIX", getRandomColor());
        allHighlightedWords += "MOINSDIX";
    }
    else
    {
        highlightWord("MOINS", getRandomColor());
        highlightWord("CINQ", getRandomColor());
        allHighlightedWords += "MOINSCINQ";
    }

    if (allLastHighlightedWords != allHighlightedWords)
    {
        clockDisplayHAL->show();
        allLastHighlightedWords = allHighlightedWords;
    }
}
