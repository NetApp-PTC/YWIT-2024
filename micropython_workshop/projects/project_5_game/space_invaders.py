"""
This script implements a (simple) game of space invaders using an attached
I2C OLED screen and a couple of buttons
"""

from machine import Pin, I2C
import ssd1306
import time

i2c = I2C(-1, scl=Pin(2), sda=Pin(0))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
left_button = Pin(5, Pin.IN)
right_button = Pin(4, Pin.IN)
fire_button = Pin(14, Pin.IN)
missles = []


class Missle:
    """Keeps track of an on-screen missle"""

    def __init__(self, x, y):
        """Save our starting state"""
        self.x = x
        self.y = y
        self.active = True

    def move(self):
        """If we move above the top of the screen, mark
        ourselves as not active. The game loop should
        cleanup any non-active missles.
        """

        self.y -= 5
        if self.y < 0:
            self.active = False

    def draw(self):
        """Draw ourselves at our current posistion"""
        for y_offset in range(5):
            oled.pixel(self.x, self.y - y_offset, 1)


class Ship:
    """Keep track of the player's ship"""

    def __init__(self, x, y):
        """Save our initial state"""
        self.x = x
        self.y = y
        self.last_fired = time.ticks_ms()

    def move(self):
        """Move left or right depending on which button is pressed"""

        if left_button.value():
            self.x -= 3
        if right_button.value():
            self.x += 3
        if self.x > 119:
            self.x = 119
        if self.x < 9:
            self.x = 9

    def draw(self):
        """Draw the pixels of our ship"""

        for y_offset in range(1, 12):
            oled.pixel(self.x, self.y - y_offset, 1)
        for y_offset in range(2, 9):
            oled.pixel(self.x + 1, self.y - y_offset, 1)
            oled.pixel(self.x - 1, self.y - y_offset, 1)
        for y_offset in range(3, 7):
            oled.pixel(self.x + 2, self.y - y_offset, 1)
            oled.pixel(self.x - 2, self.y - y_offset, 1)
        for y_offset in range(6, 3, -1):
            inner_offset = y_offset
            for x_offset in range(3, 10):
                oled.pixel(self.x - x_offset, self.y - inner_offset, 1)
                oled.pixel(self.x + x_offset, self.y - inner_offset, 1)
                inner_offset -= 1
        for y_offset in range(2, 6):
            oled.pixel(self.x - 8, self.y - y_offset, 1)
            oled.pixel(self.x + 8, self.y - y_offset, 1)
        for y_offset in range(5, 9):
            oled.pixel(self.x - 5, self.y - y_offset, 1)
            oled.pixel(self.x + 5, self.y - y_offset, 1)

    def fire(self):
        """If the fire button is pressed and the cooldown time has
        passed, then generate a new missle object at our current position
        """

        now = time.ticks_ms()
        if fire_button.value() and now - self.last_fired > 200:
            self.last_fired = now
            missles.append(Missle(self.x, self.y - 10))


def update_missles():
    """Remove any non-active missles and move the rest"""

    global missles
    missles = [m for m in missles if m.active]
    for missle in missles:
        missle.move()
        missle.draw()


def game_loop(ship):
    """Drive the main game loop"""

    oled.fill(0)
    ship.fire()
    update_missles()
    ship.move()
    ship.draw()
    oled.show()

try:
    ship = Ship(64, 64)
    while True:
        game_loop(ship)
except KeyboardInterrupt:
    pass
