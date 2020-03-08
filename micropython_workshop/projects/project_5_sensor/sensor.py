"""
This program uses a DHT11 temperature and humidity sensor. It will
periodically take measurements and report the values. The information
will be printed to the serial connection and optionally to an ss1306
OLED screen.
"""

import dht
from machine import Pin, I2C
import ssd1306
import time

USE_OLED = True

# set up the DHT11 sensor's data pin
d = dht.DHT11(Pin(0))

if USE_OLED:
    # create an I2C device with the clock on pin 5 and the data on pin 4
    i2c = I2C(-1, scl=Pin(5), sda=Pin(4))
    # set up the OLED screen with a width of 128 and height of 64 and
    # attach it to our I2C pins
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)

while True:
    # take a measurement and retrieve the temperature and humidity
    d.measure()
    temp_f = d.temperature() * 9/5 + 32
    humidity = d.humidity()

    # output the values to the serial console
    temp_str = "Temp: %s" % temp_f
    humid_str = "Hum : %s" % humidity
    print(temp_str)
    print(humid_str)

    # optionally output the values to our screen
    if USE_OLED:
        oled.fill(0)
        oled.text(temp_str, 0, 0)
        oled.text(humid_str, 0, 10)
        oled.show()

    # the DHT11 device can at most retrieve 1 sample each second
    # but we're going to only poll once every 5 seconds
    time.sleep(5)

