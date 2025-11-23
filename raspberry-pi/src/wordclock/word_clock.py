import random
from datetime import datetime
from gif import display_gif
from clock_display_hal import ClockDisplayHAL


class WordClock:
    COLORS = [
        (255, 0, 0),  # Red
        (0, 255, 0),  # Green
        (0, 0, 255),  # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
        (255, 255, 255),  # White
        (165, 42, 42),  # Brown
    ]

    def __init__(self, clock_display_hal,gif_path):
        self.last_hour = -1
        self.all_last_highlighted_words = ""
        self.clock_display_hal = clock_display_hal
        self.gif_path=gif_path

    def highlight_word(self, word, color=(255, 255, 255)):
        if word in ClockDisplayHAL.WORDS_TO_LEDS:
            self.clock_display_hal.display_word(word, color)
        
    def get_random_color(self):
        return random.choice(WordClock.COLORS)

    def add_highlighted_word(self, word):
        self.highlight_word(word, self.get_random_color())
        self.all_last_highlighted_words += word

    def display_time(self):
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        self.clock_display_hal.clear_pixels(show=False)
        if hour != self.last_hour and self.gif_path:
            if minute == 0:
                display_gif(self.gif_path,self.clock_display_hal)
                self.clock_display_hal.clear_pixels(show=False)
                self.last_hour = hour

        self.add_highlighted_word("IL")
        self.add_highlighted_word("EST")
        all_highlighted_words = "ILEST"

        # Handle hours
        if hour == 0 :
            self.add_highlighted_word("MINUIT")
            all_highlighted_words += "MINUIT"
        elif hour == 12:
            self.add_highlighted_word("MIDI")
            all_highlighted_words += "MIDI"
        else:
            hour = now.hour % 12
            self.add_highlighted_word(f"HEURE_{hour}")
            all_highlighted_words += f"HEURE_{hour}"

            h = "HEURES" if hour != 1 else "HEURE"
            self.add_highlighted_word(h)
            all_highlighted_words += h


        # Handle minutes
        if minute < 5:
            self.add_highlighted_word("PILE")
            all_highlighted_words += "PILE"
        elif minute < 10:
            self.add_highlighted_word("CINQ")
            all_highlighted_words += "CINQ"
        elif minute < 15:
            self.add_highlighted_word("DIX")
            all_highlighted_words += "DIX"
        elif minute < 20:
            self.add_highlighted_word("ET")
            self.add_highlighted_word("QUART")
            all_highlighted_words += "ETQUART"
        elif minute < 25:
            self.add_highlighted_word("VINGT")
            all_highlighted_words += "VINGT"
        elif minute < 30:
            self.add_highlighted_word("VINGTCINQ")
            all_highlighted_words += "VINGTCINQ"
        elif minute < 35:
            self.add_highlighted_word("ET")
            self.add_highlighted_word("DEMI")
            all_highlighted_words += "ETDEMI"
        elif minute < 40:
            self.add_highlighted_word("MOINS")
            self.add_highlighted_word("VINGT")
            self.add_highlighted_word("CINQ")
            all_highlighted_words += "MOINSVINGTCINQ"
        elif minute < 45:
            self.add_highlighted_word("MOINS")
            self.add_highlighted_word("VINGT")
            all_highlighted_words += "MOINSVINGT"
        elif minute < 50:
            self.add_highlighted_word("MOINS")
            self.add_highlighted_word("LE")
            self.add_highlighted_word("QUART")
            all_highlighted_words += "MOINSLEQUART"
        elif minute < 55:
            self.add_highlighted_word("MOINS")
            self.add_highlighted_word("DIX")
            all_highlighted_words += "MOINSDIX"
        else:
            self.add_highlighted_word("MOINS")
            self.add_highlighted_word("CINQ")
            all_highlighted_words += "MOINSCINQ"

        # Update display only if there are changes
        if self.all_last_highlighted_words != all_highlighted_words:
            self.clock_display_hal.show()
            self.all_last_highlighted_words = all_highlighted_words
