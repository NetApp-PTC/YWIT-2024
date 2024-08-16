"""
This program uses an AHT10 temperature and humidity sensor. it will
periodically take measurements and report the values. The information
will be pritned to the console.
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

# I2C is a type of protocol. That is, a language that two devices can use
# to communicate with each other. The SoftI2C class allows us to define
# which pins on the microcontroller that we are using and returns an interface
# we can use in code to read and write messages to each device.
i2c = SoftI2C(scl=Pin(7), sda=Pin(6))

# This tells the ahtx0 library that we have connected our device to
# the pins we have defined above
sensor = ahtx0.AHT10(i2c)

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
    print(f"\nTemperature: {celcius:0.2f} °C, {fahrenheit:0.2f} °F")
    print(f"Humidity: {humidity:0.2f} %")

    # wait a few seconds for the sensor to reset and then loop again
    time.sleep(5)
