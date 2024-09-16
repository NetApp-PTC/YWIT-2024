"""
This module holds the sprite information for the entities in the game
"""

import framebuf

ENEMY_SPRITE1 = framebuf.FrameBuffer(
    bytearray([
        0b00001000, 0b00100000,
        0b00000100, 0b01000000,
        0b00001111, 0b11100000,
        0b00011011, 0b10110000,
        0b00111111, 0b11111000,
        0b00101111, 0b11101000,
        0b00101000, 0b00101000,
        0b00000110, 0b11000000,
    ]), 16, 8, framebuf.MONO_HLSB,
)

ENEMY_SPRITE2 = framebuf.FrameBuffer(
    bytearray([
        0b00001000, 0b00100000,
        0b00100100, 0b01001000,
        0b00101111, 0b11101000,
        0b00111011, 0b10111000,
        0b00111111, 0b11111000,
        0b00001111, 0b11100000,
        0b00001000, 0b00100000,
        0b00010000, 0b00010000,
    ]), 16, 8, framebuf.MONO_HLSB,
)

SHIP_SPRITE = framebuf.FrameBuffer(
    bytearray([
        0b00000001, 0b00000000,
        0b00000011, 0b10000000,
        0b00011111, 0b11110000,
        0b00111111, 0b11111000,
        0b00111111, 0b11111000,
    ]), 16, 5, framebuf.MONO_HLSB,
)
