from machine import Pin, SPI
import st7789py as st7789
import time
from fonts import font

spi = SPI(
    1,
    baudrate=40000000,
    polarity=1,
    phase=1,
    sck=Pin(14),
    mosi=Pin(15)
)

backlight = Pin(20, Pin.OUT)
backlight.value(0)

DISPLAY_W = 240
DISPLAY_H = 240
tft = st7789.ST7789(
    spi,
    DISPLAY_W,
    DISPLAY_H,
    reset=Pin(17, Pin.OUT),
    dc=Pin(16, Pin.OUT),
    backlight=backlight,
    rotation=0
)

red = st7789.color565(255, 0, 0)
green = st7789.color565(0, 255, 0)
blue = st7789.color565(0, 0, 255)
black = st7789.color565(0, 0, 0)
white = st7789.color565(255, 255, 255)


FONT_WIDTH = 8
FONT_HEIGHT = 16

def clear_whole_line(): 
    tft.fill_rect(0, 120 - FONT_HEIGHT, DISPLAY_W, FONT_HEIGHT*2, black)

def clear_two_whole_lines(): 
    tft.fill_rect(0, 120 - FONT_HEIGHT, DISPLAY_W, FONT_HEIGHT*4, black)

def render_text_line_center(text, color): 
    x = 120 - len(text)*FONT_WIDTH
    y = 120 - FONT_HEIGHT
    tft.text(font, text, x, y, color)

def render_two_text_lines_center(text1, text2, color): 
    tft.text(font, text1, 120-(len(text1)*FONT_WIDTH), 120-FONT_HEIGHT, color)
    tft.text(font, text2, 120-(len(text2)*FONT_WIDTH), 120+FONT_HEIGHT, color)


def boot():
    render_text_line_center("Arch mini", white)
    time.sleep(2)
    clear_whole_line()
    render_two_text_lines_center("Made with love", "By N", white)
    time.sleep(2)
    clear_two_whole_lines()
    render_text_line_center("Booting up", white)
    booting_text = [
        "Booting up.",
        "Booting up..",
        "Booting up...",
    ]

    booting_counter = 0
    while booting_counter <= 5:
        index = booting_counter%len(booting_text)
        if(index == 0):
            clear_whole_line()
        text = booting_text[index]
        render_text_line_center(text, white)
        booting_counter += 1
        time.sleep(1)

    clear_whole_line()

    render_two_text_lines_center("Welcome", "Ecenur", green)

boot()
