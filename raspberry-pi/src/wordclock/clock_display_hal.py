import board
import neopixel

"""
Clock Display Hardware Abstraction Layer

Display letters and indexes
131 ILFESTAMMIDI 120
108 BESTGMUMWDIX 119
107 BQUATREHNEUF 096
084 TROISSIXCINQ 095
083 PSEPTGDEUXHR 072
060 JUNEKMINUITE 071
059 ALONZEIHUITX 048
036 HEURESAMOINS 047
035 PILETHQUARTZ 024
012 ADIXBOUDEMIY 023
011 VINGTKLVCINQ 000

131 IL.EST..MIDI 120
108 .........DIX 119
107 .QUATRE.NEUF 096
084 TROISSIXCINQ 095
083 .SEPT.DEUX.. 072
060 .UNE.MINUIT. 071
059 ..ONZE.HUIT. 048
036 HEURES.MOINS 047
035 PILET.QUART. 024
012 .DIX...DEMI. 023
011 VINGT...CINQ 000
"""
class ClockDisplayHAL:
    WIDTH = 12
    HEIGHT = 11
    NUM_LEDS = WIDTH * HEIGHT
    xx = 0

    WORDS_TO_LEDS = {
        "DEMI": (19, 22),
        "QUART": (25, 29),
        "CINQ": (0, 3),
        "DIX": (13, 15),
        "VINGT": (7, 11),
        "ET": (31, 32),
        "LE": (32, 33),
        "MOINS": (43, 47),
        "PILE": (32, 35),
        "HEURE": (36, 40),
        "HEURES": (36, 41),
        "HEURE_1": (61, 63),
        "HEURE_2": (74, 77),
        "HEURE_3": (84, 88),
        "HEURE_4": (101, 106),
        "HEURE_5": (92, 95),
        "HEURE_6": (89, 91),
        "HEURE_7": (82, 79),
        "HEURE_8": (49, 52),
        "HEURE_9": (96, 99),
        "HEURE_10": (117, 119),
        "HEURE_11": (54, 57),
        "MIDI": (120, 123),
        "MINUIT": (65, 70),
        "EST": (126, 128),
        "IL": (130, 131),
    }

    def __init__(self, board_pin, brightness):
        self.pixels = neopixel.NeoPixel(getattr(board, board_pin), self.NUM_LEDS, brightness=brightness, auto_write=False)

    def display_word(self, word, color):
        start, end = ClockDisplayHAL.WORDS_TO_LEDS[word]
        for i in range(start, end + 1):
            self.pixels[i] = color

    def cartesian_to_word_clock_led_strip_index(self, x, y):
        if y % 2 == 0:
            row_index = ClockDisplayHAL.NUM_LEDS - (y * ClockDisplayHAL.WIDTH)
            index = row_index - (x + 1)
        else:
            row_index = ClockDisplayHAL.NUM_LEDS - ((y + 1) * ClockDisplayHAL.WIDTH)
            index = row_index + x
        if index < 0 or index >= ClockDisplayHAL.NUM_LEDS:
            raise ValueError(f"Invalid x={x}, y={y}. Hardware only supports x=0-11, y=0-10")
        return index

    def set_pixel(self, x, y, color, width=12):
        index = self.cartesian_to_word_clock_led_strip_index(x, y)
        self.pixels[index] = color

    def clear_pixels(self, show=True):
        self.pixels.fill((0, 0, 0))
        if show:
            self.pixels.show()

    def show(self):
        self.pixels.show()
