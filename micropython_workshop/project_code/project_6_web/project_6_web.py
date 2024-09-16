"""
This example shows how to use the WiFi connection to connect to
an internet server and pull information to display on the screen. It makes use
of several freely available APIs and parses their responses to display relevant
information based on the current date, time, and weather conditions.
"""

from machine import Pin, SoftI2C
import ssd1306
import network
import time

import requests
from debounced_button import DebouncedButton


# You must provide values for these that match the WiFi network you would like to
# connect to.
NETWORK_NAME = ""
NETWORK_PASSWORD = ""

OLED: ssd1306.SSD1306_I2C
IP_ADDRESS = None
LOCATION = None
CURRENT_SCREEN = 0
SCREENS_AVAILABLE = ["date_and_time", "weather", "calendar_events"]

# https://open-meteo.com/en/docs
_WEATHER_CODES = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing Rime Fog",
    51: "Drizzle: Light",
    53: "Drizzle: Moderate",
    55: "Drizzle: Dense",
    56: "Freezing Drizzle: Light",
    57: "Freezing Drizzle: Dense",
    61: "Rain: Slight",
    63: "Rain: Moderate",
    65: "Rain: Heavy",
    66: "Freezing Rain: Light",
    67: "Freezing Rain: Heavy",
    71: "Snow Fall: Slight",
    73: "Snow Fall: Moderate",
    75: "Snow Fall: Heavy",
    77: "Snow Grains",
    80: "Rain Showers: Slight",
    81: "Rain Showers: Moderate",
    82: "Rain Showers: Violent",
    85: "Snow Showers: Slight",
    86: "Snow Showers: Heavy",
    95: "Thunderstorm",
    96: "Thuderstorm Slight Hail",
    99: "Thunderstorm Heavy Hail",
}


def connect_to_wifi():
    """Attempt to connect to the WiFi network with the credentials set above. This will loop for up
    to 10 seconds to wait for the connection to finish. If it does not finish successfully within
    that time, it may be because the password is incorrect or the network is not in range.
    """

    if not NETWORK_NAME or not NETWORK_PASSWORD:
        print("Don't forget to fill in the WiFi details at the top of the script!")
        return False

    print(f"Connecting to {NETWORK_NAME}...")
    OLED.text("Connecting...", 12, 25)
    OLED.show()

    interface = network.WLAN(network.STA_IF)
    interface.active(True)
    interface.connect(NETWORK_NAME, NETWORK_PASSWORD)
    tries = 10
    while tries > 0:
        if not interface.isconnected():
            tries -= 1
            time.sleep(1)
        else:
            print(f"Connected to {NETWORK_NAME} successfully")
            break
    else:
        print(f"Failed to connect to {NETWORK_NAME}. Is the password correct?")
        return False

    return True


def change_screen_left(pin):
    """This function is called when the left button is pressed"""

    global CURRENT_SCREEN
    CURRENT_SCREEN -= 1
    if CURRENT_SCREEN < 0:
        CURRENT_SCREEN = len(SCREENS_AVAILABLE) - 1

    show_loading()
    draw_screen()


def change_screen_right(pin):
    """This function is called when the right button is pressed"""

    global CURRENT_SCREEN
    CURRENT_SCREEN += 1
    if CURRENT_SCREEN == len(SCREENS_AVAILABLE):
        CURRENT_SCREEN = 0

    show_loading()
    draw_screen()


def show_loading():
    """This is called when we want to draw a loading screen to let the user know that we are in the
    process of changing to a new screen.
    """

    title = SCREENS_AVAILABLE[CURRENT_SCREEN]
    OLED.fill(0)
    OLED.text("Loading", 17, 25)
    OLED.text(f"{title}...", 0, 35)
    OLED.show()


def draw_screen():
    """This function dynamically calls the draw function for the current screen. It relies on the
    SCREENS_AVAILABLE list matching the name of the function to call.
    """

    locals()[f"draw_{SCREENS_AVAILABLE[CURRENT_SCREEN]}"]()
    OLED.show()


def draw_date_and_time():
    """Use the timeapi.io site to fetch the current time using the IP address of our microcontroller

    API documentation at https://timeapi.io/swagger/index.html
    """
    response = requests.get(f"https://timeapi.io/api/time/current/ip?ipAddress={IP_ADDRESS}")
    date_time = response.json()
    OLED.fill(0)
    OLED.text(f"{date_time['hour']:02d}:{date_time['minute']:02d}:{date_time['seconds']:02d}", 30, 5)
    OLED.text(f"{date_time['dayOfWeek']}", 35, 15)
    OLED.text(f"{date_time['date']}", 20, 25)


def draw_weather():
    """Use the open-meteo.com site to fetch the current weather using the location of our microcontroller
    in the world (as discovered based on our IP address).

    ipapi.co docs: https://ipapi.com/documentation
    open-meteo.com docs: https://open-meteo.com/en/docs
    """
    global LOCATION
    # first get our location based on our IP_ADDRESS if we haven't looked it up before
    if not LOCATION:
        response = requests.get(f"https://ipapi.co/{IP_ADDRESS}/latlong")
        LOCATION = response.text.split(",")

    weather = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={LOCATION[0]}&" +\
        f"longitude={LOCATION[1]}&current=temperature_2m,relative_humidity_2m,weather_code"
    ).json()
    celcius = weather["current"]["temperature_2m"]
    fahrenheit = celcius * (9/5) + 32
    humidity = weather["current"]["relative_humidity_2m"]
    description = _WEATHER_CODES[weather["current"]["weather_code"]]
    OLED.fill(0)
    OLED.text(f"Temp: {celcius:0.2f} C", 0, 0)
    OLED.text(f"      {fahrenheit:0.2f} F", 0, 10)
    OLED.text(f"Humd: {humidity:0.2f} %", 0, 20)
    OLED.text(description, 0, 35)


def draw_calendar_events():
    """Use the date.nager.at API to fetch a list of US public holidays for the current month and
    display them on the screen.

    API docs: https://date.nager.at/Api
    """

    response = requests.get(f"https://timeapi.io/api/time/current/ip?ipAddress={IP_ADDRESS}")
    date_time = response.json()

    # Get a list of public holidays (currently hard-coded to just the US)
    response = requests.get(f"https://date.nager.at/api/v3/PublicHolidays/{date_time['year']}/US")

    # print out any holidays happening this month
    line = 0
    OLED.fill(0)
    for holiday in response.json():
        month = int(holiday["date"].split("-")[1])
        if date_time["month"] == month:
            OLED.text(f"{holiday['date']}:", 0, line)
            line += 10
            OLED.text(f"  {holiday['name']}", 0, line)
            line += 10

    if line == 0:
        OLED.text("No holidays", 20, 20)
        OLED.text("this month", 23, 30)


def main():
    """Set up our project by initializing the screen, connecting to WiFi and then determining our
    public facing IP address which will be needed to talk to the other APIs. We also set up our buttons
    and then loop forever waiting for inputs to switch screens. Additionally, every 5 seconds we will
    refresh the current screen that we're on.

    API docs for ipify: https://www.ipify.org/
    """
    global OLED, IP_ADDRESS

    # set up our screen
    i2c = SoftI2C(scl=Pin(7), sda=Pin(6))
    OLED = ssd1306.SSD1306_I2C(128, 64, i2c)
    OLED.fill(0)

    if not connect_to_wifi():
        return

    # We need to determine our public facing IP address (used to get the weather
    # for our location)
    IP_ADDRESS = requests.get("https://api.ipify.org").text

    # set up the buttons to call a function when pressed
    DebouncedButton(8, change_screen_left)
    DebouncedButton(20, change_screen_right)

    # run forever (or until interrupted) and refresh
    # the current screen every 5 seconds
    show_loading()
    while True:
        draw_screen()
        time.sleep(5)

main()
