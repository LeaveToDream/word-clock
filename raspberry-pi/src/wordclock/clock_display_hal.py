import board
import neopixel

"""
IT IS ONE OCLOCK
IT IS FIFTEEN PAST THREE
IT IS TWENTY TO NINE


IL EST UNE HEURE PILE
IL EST TROIS HEURES CINQ
IL EST TROIS HEURES DIX
IL EST TROIS HEURES ET QUART
IL EST TROIS HEURES VINGT
IL EST TROIS HEURES VINGT CINQ
IL EST TROIS HEURES ET DEMIE
IL EST TROIS HEURES TRENTE CINQ
IL EST TROIS HEURES MOINS VINGT
IL EST TROIS HEURES MOINS LE QUART
IL EST TROIS HEURES MOINS DIX
IL EST TROIS HEURES MOINS CINQ
IL EST DIX HEURES MOINS DIX
IL EST MINUIT
IL EST MIDI

LISTE MOTS :
_IL 
_EST 
_UNE / _DEUX / _TROIS / _QUARTRE / _CINQ /_SIX / _SEPT / _HUIT / _NEUF / _DIX / _ONZE / _MINUIT / _MIDI
_HEURE(S)
_PILE / _MOINS / _ET 
_LE
_VINGT 
_CINQ / DIX / _QUART / DEMI

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

"""
Clock Display Hardware Abstraction Layer

Display letters and indexes
131 ITLISASTHPMA 120
108 ACFIFTEENDCO 119
107 TWENTYFIVEXW 096
084 THIRTYXTENXW 095
083 MINUTESETOUR 072
060 PASTORUFOURT 071
059 SEVENXTWELVE 048
036 NINEFIVECTWO 047
035 EIGHTFELEVEN 024
012 SIXTHREEONEG 023
011 TENSEZOCLOCK 000
"""
class ClockDisplayHAL:
    WIDTH = 12
    HEIGHT = 11
    NUM_LEDS = WIDTH * HEIGHT
    xx = 0

    WORDS_TO_LEDS = {
        "DEMI": (xx, xx),
        "QUART": (xx, xx),
        "CINQ": (xx, xx),
        "DIX": (xx, xx),
        "VINGT": (xx, xx),
        "ET": (xx, xx),
        "LE": (xx, xx),
        "MOINS": (xx, xx),
        "PILE": (xx, xx),
        "HEURE": (xx, xx),
        "HEURES": (xx, xx),
        "HEURE_1": (xx, xx),
        "HEURE_2": (xx, xx),
        "HEURE_3": (xx, xx),
        "HEURE_4": (101, 106),
        "HEURE_5": (xx, xx),
        "HEURE_6": (xx, xx),
        "HEURE_7": (xx, xx),
        "HEURE_8": (xx, xx),
        "HEURE_9": (96, 99),
        "HEURE_10": (117, 119),
        "HEURE_11": (xx, xx),
        "MIDI": (120, 123),
        "MINUIT": (xx, xx),
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
