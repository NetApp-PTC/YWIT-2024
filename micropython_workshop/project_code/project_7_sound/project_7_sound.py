from collections import OrderedDict
from machine import Pin, PWM
import time

# frequencies of notes (based on A=440Hz)
NOTES = OrderedDict([
    ("A0", 110),
    ("Bb0", 117),
    ("B0", 123),
    ("C0", 131),
    ("C#0", 139),
    ("D0", 147),
    ("Eb0", 156),
    ("E0", 165),
    ("F0", 173),
    ("F#0", 185),
    ("G0", 196),
    ("G#0", 208),
    ("A1", 220),
    ("Bb1", 233),
    ("B1", 247),
    ("C1", 262), # middle C
    ("C#1", 277),
    ("D1", 294),
    ("Eb1", 311),
    ("E1", 330),
    ("F1", 349),
    ("F#1", 370),
    ("G1", 392),
    ("G#1", 415),
    ("A2", 440),
    ("Bb2", 466),
    ("B2", 494),
    ("C2", 523), # C inside the staff
    ("C#2", 554),
    ("D2", 587),
    ("Eb2", 622),
    ("E2", 659),
    ("F2", 698),
    ("F#2", 740),
    ("G2", 784),
    ("G#2", 831),
    ("A3", 880),
    ("Bb3", 932),
    ("B3", 988),
    # Notes above 1KHz won't play correctly on an ESP8266 because it's only capable of 1k maximum
    # for the PWM. If these are attempted, they get clamped to 1k. They will work fine on the ESP32
    # though since it can go up to 40MHz!
    ("C3", 1047), # C above the staff
    ("C#3", 1109),
    ("D3", 1175),
    ("Eb3", 1245),
    ("E3", 1319),
    ("F3", 1397),
    ("F#3", 1480),
    ("G3", 1577),
    ("G#3", 1661),
])

# @ 60bpm
DURATIONS = {
    "thirty_second": 125,
    "sixteenth": 250,
    "triplet_eighth": 333,
    "eighth": 500,
    "dotted_eighth": 725,
    "triplet_quarter": 667,
    "quarter": 1000,
    "dotted_quarter": 1500,
    "half": 2000,
    "dotted_half": 3000,
    "whole": 4000,
}

INSTRUMENTS = {
    "trumpet": 64,
    "clarinet": 512,
    "keyboard": 700,
}

def tone(pins, note=None, duration=1000, instrument="clarinet"):
    """Play a note by setting the provided pins up as
    a PWM device with the necessary frequency.

    Args:
        pins: A list of pin objects. All pins will be
            set to the same note (meant for playing
            audio in a left and a right channel).
        note: Either an integer or a string that can
            be mapped by the global NOTES dictionary.
        duration: An integer which represents the
            number of milliseconds to play the tone.
        instrument: This setting changes the duty cycle
            of the PWM object. By changing the duty cycle,
            the resulting sound changes. The sounds mapped
            by the INSTRUMENTS dictionary are what the
            duty cycles sounded like to me though my headphones
            when writing this.
    """

    print('playing %s for %s' % (note, duration))

    # if this is a rest, then just sleep
    if not note:
        time.sleep_ms(duration)
        return

    # if we were given a string note, find the frequency
    note = NOTES.get(note, note)
    instrument = INSTRUMENTS.get(instrument, instrument)

    # set the notes and sleep for the appropriate time
    pwms = [PWM(pin, freq=note, duty=instrument) for pin in pins]
    time.sleep_ms(duration)

    # stops the notes playing
    for pwm in pwms:
        pwm.deinit()

# set up the globals
tempo = 130
instrument = "clarinet"
speaker = Pin(6, Pin.OUT)

# import the song and play each note
from legend_of_zelda import SONG

try:
    for note in SONG:
        duration = int(DURATIONS[note[1]] * (60 / tempo))
        tone([speaker], note[0], duration=duration, instrument=instrument)
except Exception:
    pwms = [PWM(pin) for pin in [speaker]]
    for pwm in pwms:
        pwm.deinit()
