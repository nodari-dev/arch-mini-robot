from machine import Pin, SPI
import st7789py as st7789
import time
import framebuf
from fonts import font

spi = SPI(
    1,
    baudrate=40000000,
    polarity=1,
    phase=1,
    sck=Pin(14),
    mosi=Pin(15)
)

backlight = Pin(9, Pin.OUT)
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

BLACK = st7789.color565(0, 0, 0)
WHITE = st7789.color565(255, 255, 255)
RED = 0xFF1919
GREEN = st7789.color565(251,104,105)


FONT_WIDTH = 8
FONT_HEIGHT = 16

def clear_whole_line(): 
    tft.fill_rect(0, 120 - FONT_HEIGHT, DISPLAY_W, FONT_HEIGHT*2, BLACK)

def clear_two_whole_lines(): 
    tft.fill_rect(0, 120 - FONT_HEIGHT, DISPLAY_W, FONT_HEIGHT*4, BLACK)

def render_text_line_center(text, color): 
    x = 120 - len(text)*FONT_WIDTH
    y = 120 - FONT_HEIGHT
    tft.text(font, text, x, y, color)

def render_two_text_lines_center(text1, text2, color): 
    tft.text(font, text1, 120-(len(text1)*FONT_WIDTH), 120-FONT_HEIGHT, color)
    tft.text(font, text2, 120-(len(text2)*FONT_WIDTH), 120+FONT_HEIGHT, color)


def boot():
    render_text_line_center("Arch mini", WHITE)
    time.sleep(2)
    clear_whole_line()
    render_two_text_lines_center("Made with love", "By N", WHITE)
    time.sleep(2)
    clear_two_whole_lines()
    render_text_line_center("Booting up", WHITE)
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
        render_text_line_center(text, WHITE)
        booting_counter += 1
        time.sleep(1)

    clear_whole_line()

    render_two_text_lines_center("Welcome", "Ecenur", GREEN)
    time.sleep(2)
    clear_two_whole_lines()

# boot()


buffer = bytearray(DISPLAY_W * DISPLAY_H * 2)

fb = framebuf.FrameBuffer(
    buffer,
    DISPLAY_W,
    DISPLAY_H,
    framebuf.RGB565
)

# tft.fill_rect(149, (240 - 90) // 2, 50, 90, WHITE)
fb.fill(RED)        # black

tft.blit_buffer(buffer, 0, 0, DISPLAY_W, DISPLAY_H)

DEFAULT_EYE_W = 60
DEFAULT_EYE_H = 90

class Eye:
  w = DEFAULT_EYE_W
  h = DEFAULT_EYE_H
  x = 5
  y = 120 - DEFAULT_EYE_H//2

def draw_eye(fb, x, y, w, h, r, color):
    for i in range(h):
        if i < r:
            offset = int((r*r - (r-i)*(r-i))**0.5)
        elif i >= h - r:
            dy = i - (h - r)
            offset = int((r*r - dy*dy)**0.5)
        else:
            offset = r

        fb.hline(x + r - offset, y + i, w - 2*(r - offset), color)

def render_eyes(eye_height, x1=50, x2=140, y1 = 0, y2 = 0):
    fb.fill(0)

    y1 = 120 - eye_height//2 if y1 == 0 else y1
    y2 = 120 - eye_height//2 if y2 == 0 else y2

    # left eye
    draw_eye(fb, x1, y1, 60, eye_height, 10, WHITE)

    # right eye
    draw_eye(fb, x2, y2, 60, eye_height, 10, WHITE)

    tft.blit_buffer(buffer, 0, 0, DISPLAY_W, DISPLAY_H)


def look_around():
    starter_x1 = 50
    starter_x2 = 140
    render_eyes(90, starter_x1, starter_x2)
    time.sleep(0.05)
    for x in range(2, 10, 2):
        starter_x1 -= x
        starter_x2 -= x
        render_eyes(eye_height=90, x1=starter_x1, x2=starter_x2)
        time.sleep(0.0001)

    time.sleep(0.5)
    for x in range(2, 13, 2):
        starter_x1 += x
        starter_x2 += x
        render_eyes(eye_height=90, x1=starter_x1, x2=starter_x2)
        time.sleep(0.0005)

    time.sleep(0.5)
    # FIX ME I HAVE BED PIXEL POSITION
    for x in range(2, 9, 1):
        starter_x1 -= x
        starter_x2 -= x
        render_eyes(eye_height=90, x1=starter_x1, x2=starter_x2)
        time.sleep(0.0005)

    time.sleep(0.5)

def squeeze_eyes():
    for h in range(90, 15, -10):
        render_eyes(h)
        time.sleep(0.0001)
    # for h in range(20, 90, 10):
    #     render_normal_eyes(h)
    #     time.sleep(0.0001)


def starting_eyes():
    render_eyes(5)
    time.sleep(1)

    # try to open eyes
    for h in range(5, 20, 1):
        render_eyes(h)
        time.sleep(0.001)

    for h in range(20, 5, -1):
        render_eyes(h)
        time.sleep(0.001)

    time.sleep(1)

    for h in range(5, 20, 1):
        render_eyes(h)
        time.sleep(0.001)
    time.sleep(1)

    for h in range(20, 5, -1):
        render_eyes(h)
        time.sleep(0.001)

    time.sleep(2.5)

    # Open eyes fully
    for h in range(5, 90, 3):
        render_eyes(h)
        time.sleep(0.001)

    # Blink couple of times to open eyes
    time.sleep(1)
    for h in range(90, 5, -10):
        render_eyes(h)
        time.sleep(0.0001)
    for h in range(5, 90, 10):
        render_eyes(h)
        time.sleep(0.0001)

    time.sleep(0.05)
    for h in range(90, 5, -10):
        render_eyes(h)
        time.sleep(0.0001)

    for h in range(5, 90, 10):
        render_eyes(h)
        time.sleep(0.0001)


    look_around()
    squeeze_eyes()

# boot()
# starting_eyes()

render_eyes(90)

def levitate():
    for h in range(5, 10, 1):
        # render_eyes()
        time.sleep(0.0001)

# time.sleep(1)
#
# def susface():
#     time.sleep(1)
#
# susface()
# fb.fill(0)

# draw_eye(fb, (240-80)//2, (240-80)//2, 80, 80, 15, WHITE)
# tft.blit_buffer(buffer, 0, 0, DISPLAY_W, DISPLAY_H)

# for h in range(1, 20, 1):
#     fb.fill(0)
#     time.sleep(0.0001)
#     draw_eye(fb, (240-80-h)//2, (240-80-h)//2, 80-h, 80-h, 15, WHITE)
#     tft.blit_buffer(buffer, 0, 0, DISPLAY_W, DISPLAY_H)
