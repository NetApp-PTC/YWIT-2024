"""
This is meant to be a very simple example of using Python
to control a piece of hardware. Here, we define a Pin object
which represents an LED that we have wired up to our
microcontroller. Then, we loop forever and toggle the state
of the Pin on and off, sleeping for half a second between
cycles.
"""

import time
from machine import Pin

# set up the Pin to control our LED. If the LED is wired
# to a different GPIO pin, then the "20" needs to be changed
# to whatever is appropriate
led = Pin(20, Pin.OUT)

try:
    while True:
        # The value of the Pin is either 1 or 0. Here we are
        # setting the value to whatever the current value is
        # not, therefore it constantly switches back and forth
        led.value(not led.value())

        # Before looping again, let's sleep for half a second
        # so that our LED stays on or off for a bit
        time.sleep(.5)
except KeyboardInterrupt:
    # We're catching the exception if the user sends a ctrl+c
    # signal through the REPL
    pass
