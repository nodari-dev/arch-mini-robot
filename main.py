from machine import Pin, SPI
import st7789py as st7789
import time
import framebuf
from fonts import font
import random

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
RED = st7789.color565(255, 0, 0)
GREEN = st7789.color565(251,104,105)

FONT_WIDTH = 8
FONT_HEIGHT = 16

buffer = bytearray(DISPLAY_W * DISPLAY_H * 2)

fb = framebuf.FrameBuffer(
    buffer,
    DISPLAY_W,
    DISPLAY_H,
    framebuf.RGB565
)

tft.blit_buffer(buffer, 0, 0, DISPLAY_W, DISPLAY_H)

DEFAULT_EYE_W = 60
DEFAULT_EYE_H = 90

DEFAULT_LEFT_EYE_X = 50
DEFAULT_RIGHT_EYE_X = 140

DEFAULT_EYE_Y = 120 - DEFAULT_EYE_H//2

LOOK_MOVEMENT_RANGE = 10
LOOK_MOVEMENT_STEP = 2

class Eye:
  w = DEFAULT_EYE_W
  h = DEFAULT_EYE_H
  x = 0
  y = DEFAULT_EYE_Y

LEFT_EYE = Eye()
RIGHT_EYE = Eye()

def clear_whole_line(): 
    tft.fill_rect(0, 120 - FONT_HEIGHT, DISPLAY_W, FONT_HEIGHT*2, BLACK)

def clear_two_whole_lines(): 
    tft.fill_rect(0, 120 - FONT_HEIGHT, DISPLAY_W, FONT_HEIGHT*4, BLACK)

def clear_three_whole_lines(): 
    tft.fill_rect(0, 120 - FONT_HEIGHT, DISPLAY_W, FONT_HEIGHT*6, BLACK)

def render_text_line_center(text, color): 
    x = 120 - len(text)*FONT_WIDTH
    y = 120 - FONT_HEIGHT
    tft.text(font, text, x, y, color)

def render_two_text_lines_center(text1, text2, color): 
    tft.text(font, text1, 120-(len(text1)*FONT_WIDTH), 120-FONT_HEIGHT, color)
    tft.text(font, text2, 120-(len(text2)*FONT_WIDTH), 120+FONT_HEIGHT, color)

def render_three_text_lines_center(text1, text2, text3, color): 
    tft.text(font, text1, 120-(len(text1)*FONT_WIDTH), 120-FONT_HEIGHT*3, color)
    tft.text(font, text2, 120-(len(text2)*FONT_WIDTH), 120, color)
    tft.text(font, text3, 120-(len(text3)*FONT_WIDTH), 120+FONT_HEIGHT*3, color)

def greeting():
    fb.fill(0)
    tft.blit_buffer(buffer, 0, 0, DISPLAY_W, DISPLAY_H)
    render_text_line_center("Hi cutie :)", WHITE)
    time.sleep(2)
    clear_whole_line()

def you_beatiful():
    fb.fill(0)
    tft.blit_buffer(buffer, 0, 0, DISPLAY_W, DISPLAY_H)
    texts = [
            ["You look",  "beautiful", "today :)"],
            ["You look",  "cute", "today"],
            ["You are", "so so", "gorgeous"],
            ["Your smile", "brings", "happines"],
            ["You have", "amazing", "smile"],
            ["You have", "beautiful", "eyes"]
    ]
    lines = random.choice(texts)
    render_three_text_lines_center(lines[0], lines[1], lines[2], WHITE)

def happy_birthday():
    fb.fill(0)
    tft.blit_buffer(buffer, 0, 0, DISPLAY_W, DISPLAY_H)
    now = time.localtime()
    # if today.month == 4 and today.day == 22:
    # if (now[1], now[2]) == (2, 19):
        # fb.fill(0)
        # tft.blit_buffer(buffer, 0, 0, DISPLAY_W, DISPLAY_H)
        # render_two_text_lines_center("Happy", "birthday!", WHITE)
        # time.sleep(2)
        # clear_whole_line()

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

    render_two_text_lines_center("Welcome", "Ecenur", WHITE)
    time.sleep(2)
    clear_two_whole_lines()


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

def fill_circle(fb, cx, cy, r, color):
    for y in range(-r, r+1):
        for x in range(-r, r+1):
            if x*x + y*y <= r*r:
                fb.pixel(cx + x, cy + y, color)

def fill_triangle(fb, x1, y1, x2, y2, x3, y3, color):
    points = sorted([(x1,y1), (x2,y2), (x3,y3)], key=lambda p: p[1])
    x1,y1 = points[0]
    x2,y2 = points[1]
    x3,y3 = points[2]

    def interp(y, y0, x0, y1, x1):
        if y1 == y0:
            return x0
        return int(x0 + (y - y0) * (x1 - x0) / (y1 - y0))

    for y in range(y1, y3+1):
        if y < y2:
            xa = interp(y, y1, x1, y3, x3)
            xb = interp(y, y1, x1, y2, x2)
        else:
            xa = interp(y, y1, x1, y3, x3)
            xb = interp(y, y2, x2, y3, x3)

        if xa > xb:
            xa, xb = xb, xa

        fb.hline(xa, y, xb - xa, color)

def draw_heart(fb, cx, cy, size, color):
    r = size // 2

    fill_circle(fb, cx - r//2 - 1//2, cy - r//2 + 2, r//2 + 2, color)
    fill_circle(fb, cx + r//2 - 1//2 , cy - r//2 + 2, r//2 + 2, color)

    fill_triangle(
        fb,
        cx - r, cy - r//4,
        cx + r, cy - r//4,
        cx,     cy + r,
        color
    )

def render_hearts():
    fb.fill(0)

    draw_heart(fb, 80, 120, 70, WHITE)
    draw_heart(fb, 160, 120, 70, WHITE)

    tft.blit_buffer(buffer, 0, 0, 240, 240)

def render_eyes(
        height1=DEFAULT_EYE_H,
        width1=DEFAULT_EYE_W,
        height2=DEFAULT_EYE_H,
        width2=DEFAULT_EYE_W,
        x1=50, x2=140, y1 = 0, y2 = 0
    ):
    fb.fill(0)

    y1 = 120 - height1//2 if y1 == 0 else y1
    y2 = 120 - height2//2 if y2 == 0 else y2

    # left eye
    LEFT_EYE.x = x1
    LEFT_EYE.y = y1
    LEFT_EYE.w = width1
    LEFT_EYE.h = height1
    draw_eye(fb, x1, y1, width1, height1, 10, WHITE)

    # right eye
    RIGHT_EYE.x = x2
    RIGHT_EYE.y = y2
    RIGHT_EYE.w = width2
    RIGHT_EYE.h = height2
    draw_eye(fb, x2, y2, width2, height2, 10, WHITE)


    tft.blit_buffer(buffer, 0, 0, DISPLAY_W, DISPLAY_H)

def sign(value):
    return (value > 0) - (value < 0)

def center_back():
    diff_y = DEFAULT_EYE_Y - LEFT_EYE.y
    diff_x = DEFAULT_LEFT_EYE_X - LEFT_EYE.x
    dy = sign(diff_y)
    dx = sign(diff_x)
    look_to(dx, dy)

DIRECTIONS = {
    "left": (-1, 0),
    "right": (1, 0),
    "top": (0, -1),
    "bottom": (0, 1),
    "top_left": (-1, -1),
    "top_right": (1, -1),
    "bottom_left": (-1, 1),
    "bottom_right": (1, 1),
}

def look_to(dx, dy):
    x = 0
    y = 0

    while abs(x) <= LOOK_MOVEMENT_RANGE and abs(y) <= LOOK_MOVEMENT_RANGE:
        render_eyes(
            y1=LEFT_EYE.y + y,
            x1=LEFT_EYE.x + x,
            y2=RIGHT_EYE.y + y,
            x2=RIGHT_EYE.x + x
        )

        x += dx * LOOK_MOVEMENT_STEP
        y += dy * LOOK_MOVEMENT_STEP

        time.sleep(0.001)

def look_around():

    dx1, dy1 = random.choice(list(DIRECTIONS.values()))
    look_to(dx1, dy1)
    time.sleep(1)

    center_back()

    dx2, dy2 = random.choice(list(DIRECTIONS.values()))
    look_to(dx2, dy2)
    time.sleep(1)

    center_back()
    time.sleep(1)

def squeeze_eyes_and_back():
    for h in range(DEFAULT_EYE_H, 30, -5):
        render_eyes(height1=h, height2=h)
        time.sleep(0.0001)
    time.sleep(3)
    for h in range(30, 90, 5):
        render_eyes(height1=h, height2=h)
        time.sleep(0.0001)

def susface():
    for h in range(LEFT_EYE.h, 30, -5):
        render_eyes(height1=h)
        time.sleep(0.0001)

def blink():
    for h in range(90, 5, -16):
        render_eyes(height1=h, height2=h)
        time.sleep(0.0001)
    for h in range(5, 90, 16):
        render_eyes(height1=h, height2=h)
        time.sleep(0.0001)

    time.sleep(0.05)

def booting_eyes():
    render_eyes(height1=5, height2=5)
    time.sleep(1)

    # try to open eyes
    for h in range(5, 20, 1):
        render_eyes(height1=h, height2=h)
        time.sleep(0.001)

    for h in range(20, 5, -1):
        render_eyes(height1=h, height2=h)
        time.sleep(0.001)

    time.sleep(1)

    for h in range(5, 20, 1):
        render_eyes(height1=h, height2=h)
        time.sleep(0.001)
    time.sleep(1)

    for h in range(20, 5, -1):
        render_eyes(height1=h, height2=h)
        time.sleep(0.001)

    time.sleep(2.5)

    # Open eyes fully
    for h in range(5, 90, 3):
        render_eyes(height1=h, height2=h)
        time.sleep(0.001)

    time.sleep(1)
    blink()
    look_around()
    squeeze_eyes_and_back()
    time.sleep(1)
    render_eyes()
    # susface()



def handle_button_press():
    button = Pin(19, Pin.IN, Pin.PULL_UP)
    while True:
        if button.value() == 0:
            render_text_line_center("Button yes", WHITE)
            time.sleep(1)
        else:
            time.sleep(1)
            render_text_line_center("Button not", WHITE)


def levitate_single():
    for y in range(LEFT_EYE.y, LEFT_EYE.y+15, 1):
        render_eyes(y1=y, y2=y)
        time.sleep(0.05)

    for y in range(LEFT_EYE.y, LEFT_EYE.y-15, -1):
        render_eyes(y1=y, y2=y)
        time.sleep(0.05)

    if random.randint(0, 1) == 1:
        blink()

    for y in range(LEFT_EYE.y, LEFT_EYE.y+15, 1):
        render_eyes(y1=y, y2=y)
        time.sleep(0.05)

    for y in range(LEFT_EYE.y, LEFT_EYE.y-15, -1):
        render_eyes(y1=y, y2=y)
        time.sleep(0.05)

def levitate():
    while True:
        levitate_single()

class Mood:
    DEFAULT = 0
    HUNGRY = 1
    SLEEPING = 2
    ANGRY = 3
    TIRED = 4
    SAD = 5
    LOVING = 6
    SUS = 7

class Archi:
    action_button = Pin(19, Pin.IN, Pin.PULL_UP)
    mood = Mood.DEFAULT
    last_look_action: str | None = None
    hunger = 0
    tiredness = 0
    button_clicked = 0
    anger = 0
    annoyanse = 0

    def check_button_status(self):
        print("button check")
        if self.action_button.value() == 0:
            print("button pressed")
            time.sleep(1)

archi = Archi()
# ================= CAT IDENTITY =================
# MODES:
    # NORMAL
    # SAD
    # HUNGRY
    # ANGRY
    # LOVING
    # SLEEPING
    # SUS

def default_mood():
    archi.check_button_status()
    time.sleep(1)
    look_around_reps = random.randrange(1, 3)
    for rep in range(look_around_reps):
        archi.check_button_status()
        name, (dx, dy) = random.choice(list(DIRECTIONS.items()))
        if name == archi.last_look_action:
            archi.check_button_status()
            time.sleep(1)
            continue
        archi.last_look_action = name
        look_to(dx, dy)
        archi.check_button_status()
        time.sleep(1)
        center_back()
        archi.check_button_status()
        rep += 1

    levitate_reps = random.randrange(5, 15)
    for rep in range(levitate_reps):
        levitate_single()
        rep += 1

    time.sleep(1)

def hungry_mood():
    print("bitch I'm sleeping")

def angry_mood():
    #   1. when annoyed
    #   2. when didnt sleep well
    print("bitch I'm sleeping")

def sad_mood():
    print("bitch I'm sleeping")

def sus_mood():
    print("bitch I'm sleeping")

def sleeping_mood():
    #   1. specific time of a day
    #   2. after food
    #   3. can be woken up
    #   4. count down the tiredness
    #   5. if tiredness => 50 then angry face
    print("bitch I'm sleeping")

def tired_mood():
    print("bitch I'm tired")

def loving_mood():
    # render_hearts()
    # if pressed once -> light squise eyes 
    # if pressed twice -> more squise eyes 
    # if pressed three time -> 
        # open eyes
        # show hearts
        # show text
    print("bitch I'm sleeping")


def main():
    # boot()
    # booting_eyes()
    # greeting()
    # render_eyes()
    #
    # MAIN EVENT LOOP
    
    while True:
        if archi.mood == Mood.DEFAULT:
            archi.check_button_status()
            default_mood()

main()
# TODO: happy birthday 



