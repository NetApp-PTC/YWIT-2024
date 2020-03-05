"""
This example uses several LEDs and a button. Pressing
the button will cycle through several patterns that the
LEDs will display.
"""

from machine import Pin, PWM
import utime

from debounced_button import DebouncedButton


def cycle():
    """This pattern will turn all of the LEDS from
    left to right, then turn them all off in order
    again.
    """

    for led in leds:
        led.on()
        utime.sleep_ms(50)
    for led in leds:
        led.off()
        utime.sleep_ms(50)


def meter():
    """This pattern looks a bit like a sound level
    meter and turns all of the LEDs on from left to
    right then turns them off from right to left.
    """

    for led in leds:
        led.on()
        utime.sleep_ms(50)
    for led in reversed(leds):
        led.off()
        utime.sleep_ms(50)


def all_blink():
    """This pattern turns all the LEDs on at the
    same time, waits, and turns them all off again.
    """

    for led in leds:
        led.on()
    utime.sleep_ms(500)
    for led in leds:
        led.off()
    utime.sleep_ms(500)


def breathe():
    """This pattern causes all of the LEDs to
    breathe in and out together by changing the
    duty cycle from min to max and back again.
    """

    pwm_leds = [PWM(l) for l in leds]
    for duty in range(0, 1001):
        for pwm in pwm_leds:
            pwm.duty(duty)
        utime.sleep_ms(1)
    for duty in range(1000, -1, -1):
        for pwm in pwm_leds:
            pwm.duty(duty)
        utime.sleep_ms(1)


def bounce():
    """This pattern causes the 'active' LED to look
    like it bounces back and forth from left to right.
    """

    for index in range(0, len(leds)):
        for led in leds:
            led.off()
        leds[index].on()
        utime.sleep_ms(100)
    for index in reversed(range(0, len(leds))):
        for led in leds:
            led.off()
        leds[index].on()
        utime.sleep_ms(100)


def change_mode(pin):
    """This is the callback for when the button is pressed.
    It will reset the state of all of the LEDs and then
    change the active party mode.
    """

    global party_mode
    reset_leds()
    party_mode += 1
    if party_mode >= len(party_modes):
        party_mode = 0


def reset_leds():
    """Initialize all LEDs to off and make sure PWM mode is off"""
    for led in leds:
        led.off()
        for led in [PWM(l) for l in leds]:
            led.deinit()


# setup our LEDs
red = Pin(5, Pin.OUT)
yellow = Pin(4, Pin.OUT)
green = Pin(0, Pin.OUT)
blue = Pin(14, Pin.OUT)
leds = [red, yellow, green, blue]

# set up our button
button = DebouncedButton(12, change_mode)

# keep a list of all of the pattern functions we have
party_modes = [cycle, meter, all_blink, breathe, bounce]
party_mode = 0

reset_leds()

# now loop forever and call the currenty party function
try:
    while True:
        party_modes[party_mode]()
except KeyboardInterrupt:
    # We're catching the exception if the user sends a ctrl+c
    # signal through the REPL
    pass

