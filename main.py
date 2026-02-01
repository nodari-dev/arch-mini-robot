
from machine import Pin, SPI
import st7789py as st7789
import time

# SPI setup (SPI1)
spi = SPI(
    1,
    baudrate=40000000,
    polarity=1,
    phase=1,
    sck=Pin(14),
    mosi=Pin(15)
)

# Backlight
backlight = Pin(20, Pin.OUT)
backlight.value(0)  # turn it on

# Display setup (NO CS)
tft = st7789.ST7789(
    spi,
    240,
    240,
    reset=Pin(17, Pin.OUT),
    dc=Pin(16, Pin.OUT),
    backlight=backlight,
    rotation=0
)

red = st7789.color565(255, 0, 0)
green = st7789.color565(0, 255, 0)
blue = st7789.color565(0, 0, 255)

tft.fill(red)
time.sleep(1)
tft.fill(green)
time.sleep(1)
tft.fill(blue)                 

