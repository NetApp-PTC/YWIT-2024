"""
This program uses an AHT10 temperature and humidity sensor. it will
periodically take measurements and report the values. The information
will be pritned to the console. This version of the code also displays
the information on the SSD1306 OLED screen.
"""

import time
from machine import Pin, SoftI2C

# When you are using a complex component (something more than an LED,
# switch, button, etc.), there will often be libraries available that
# you can search for and find online. These libraries are collections
# of functions that someone else wrote code for and that you can reuse
# without having to write your own code. The ahtx0 library we are
# importing below is a library that knows how to talk to our temperature
# and humidity sensor
import ahtx0

# Here we import another library that knows how to draw things on the
# small screen that's included in the kit
import ssd1306

# I2C is a type of protocol. That is, a language that two devices can use
# to communicate with each other. The SoftI2C class allows us to define
# which pins on the microcontroller that we are using and returns an interface
# we can use in code to read and write messages to each device.
i2c_sensor = SoftI2C(scl=Pin(7), sda=Pin(6))

# create another I2C device to control our screen
i2c_oled = SoftI2C(scl=Pin(7), sda=Pin(5))

# This tells the ahtx0 library that we have connected our device to
# the pins we have defined above
sensor = ahtx0.AHT10(i2c_sensor)

# set up the OLED screen with a width of 128 and height of 64 and
# attach it to our I2C pins
oled = ssd1306.SSD1306_I2C(128, 64, i2c_oled)

# This loop will run forever and print out the current temperature and
# humidity. The sensor device we are using measures temperature in
# celcius. Our code takes that and converts it to fahrenheit and then
# prints out both values.
while True:
    # read the measurement from the sensor
    celcius = sensor.temperature
    humidity = sensor.relative_humidity

    # convert the temperature from celcius to fahrenheit
    fahrenheit = celcius * (9/5) + 32

    # print the values to the terminal
    print(f"\nTemp: {celcius:0.2f} °C, {fahrenheit:0.2f} °F")
    print(f"Humidity: {humidity:0.2f} %")

    # first, erase the previous contents of the screen (fills all pixels with black)
    oled.fill(0)

    # then write out our strings to the screen buffer
    oled.text(f"Temp: {celcius:0.2f} C", 0, 0)
    oled.text(f"      {fahrenheit:0.2f} F", 0, 10)
    oled.text(f"Humd: {humidity:0.2f} %", 0, 20)

    # finally, we have to call show so that the screen updates all of the new contents
    oled.show()

    # wait a few seconds for the sensor to reset and then loop again
    time.sleep(5)
