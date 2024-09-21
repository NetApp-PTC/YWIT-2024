"""
This example shows how you can hook up a button to change
the flow of the running program when pressed. Here we are
using the pulse width modulation feature of a Pin to change
how bright the LED appears. Each time the button is pressed,
we rotate through the list of brightness levels (0-1000) and
set the new duty cycle.

This example uses an interrupt handler (IRQ) on the Pin that
the button is attached to. When the button is pressed, a
hardware signal causes the current place in the program to
be interrupted and the callback we set to be executed before
normal control is returned.

Also note that we are using a custom DebouncedButton class.
This is due to how most buttons work. When pressed, the contacts
may bounce a few times causing multiple signals to be sent.
This is something we want to avoid so we set a small timeout
between presses.
"""

from machine import Pin, PWM

from debounced_button import DebouncedButton


# This is the list of possible values for the brightness
# of the LED that our button will cycle through. The min
# that is supported is 0 and the max is 1000
brightness_list = [0, 333, 666, 1000]
brightness = 0


def toggle_led(pin):
    """This function is used as a callback for the interrupt
    handler of the button signal. It will rotate through the
    list of brightnesses and set the new duty cycle for the Pin
    """

    global brightness
    brightness += 1
    if brightness >= len(brightness_list):
        brightness = 0
    new_duty = brightness_list[brightness]
    led.duty(new_duty)
    print("LED brightness now at %.0f%%" % (new_duty / 1000 * 100))


# set up our Pin where the LED is attached
led = PWM(Pin(20))
led.duty(0)

# set up the Pin where our button is attached
button = DebouncedButton(8, toggle_led)

print("Try pressing the button to change the brightness of the LED")
try:
    while True:
        pass
except KeyboardInterrupt:
    # We're catching the exception if the user sends a ctrl+c
    # signal through the REPL
    pass
