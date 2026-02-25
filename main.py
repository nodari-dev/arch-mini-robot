from machine import Pin, SPI
import framebuf
import random
import time
import math
from lib import st7789py as st7789
from lib import text_renderer
from lib import arch
from lib import constants
from lib import graphics

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

tft = st7789.ST7789(
    spi,
    constants.DISPLAY_W,
    constants.DISPLAY_H,
    reset=Pin(17, Pin.OUT),
    dc=Pin(16, Pin.OUT),
    backlight=backlight,
    rotation=0
)

buffer = bytearray(constants.DISPLAY_W * constants.DISPLAY_H * 2)

fb = framebuf.FrameBuffer(
    buffer,
    constants.DISPLAY_W,
    constants.DISPLAY_H,
    framebuf.RGB565
)

def flush_buffer():
    tft.blit_buffer(buffer, 0, 0, constants.DISPLAY_W, constants.DISPLAY_H)

def greeting():
    fb.fill(0)
    tft.blit_buffer(buffer, 0, 0, constants.DISPLAY_W, constants.DISPLAY_H)
    text_renderer.render_text_line_center(tft, "Hi cutie :)", constants.WHITE)
    time.sleep(2)
    text_renderer.clear_whole_line(tft)

def boot():
    text_renderer.render_text_line_center(tft, "Arch mini", constants.WHITE)
    time.sleep(2)
    text_renderer.clear_whole_line(tft)
    text_renderer.render_two_text_lines_center(tft, "Made with love", "By N", constants.WHITE)
    time.sleep(2)
    text_renderer.clear_two_whole_lines(tft)
    text_renderer.render_text_line_center(tft, "Booting up", constants.WHITE)
    booting_text = [
        "Booting up.",
        "Booting up..",
        "Booting up...",
    ]

    booting_counter = 0
    while booting_counter <= 5:
        index = booting_counter%len(booting_text)
        if(index == 0):
            text_renderer.clear_whole_line(tft)
        text = booting_text[index]
        text_renderer.render_text_line_center(tft, text, constants.WHITE)
        booting_counter += 1
        time.sleep(1)

    text_renderer.clear_whole_line(tft)

    text_renderer.render_two_text_lines_center(tft, "Welcome", "Ecenur", constants.WHITE)
    time.sleep(2)
    text_renderer.clear_two_whole_lines(tft)


archi = arch.Archi()

def render_hearts():
    fb.fill(0)

    graphics.draw_heart(fb, 80, 120, 70, constants.WHITE)
    graphics.draw_heart(fb, 160, 120, 70, constants.WHITE)

    tft.blit_buffer(buffer, 0, 0, constants.DISPLAY_W, constants.DISPLAY_H)

def render_eyes(
        height1=constants.DEFAULT_EYE_H,
        width1=constants.DEFAULT_EYE_W,
        height2=constants.DEFAULT_EYE_H,
        width2=constants.DEFAULT_EYE_W,
        x1=45, x2=135, y1 = 0, y2 = 0
    ):
    fb.fill(0)

    y1 = 120 - height1//2 if y1 == 0 else y1
    y2 = 120 - height2//2 if y2 == 0 else y2

    # left eye
    archi.left_eye.x = x1
    archi.left_eye.y = y1
    archi.left_eye.w = width1
    archi.left_eye.h = height1
    graphics.draw_eye(fb, x1, y1, width1, height1, 10, constants.WHITE)

    # right eye
    archi.right_eye.x = x2
    archi.right_eye.y = y2
    archi.right_eye.w = width2
    archi.right_eye.h = height2
    graphics.draw_eye(fb, x2, y2, width2, height2, 10, constants.WHITE)

    # tft.blit_buffer(buffer, 0, 0, constants.DISPLAY_W, constants.DISPLAY_H)

def sign(value):
    return (value > 0) - (value < 0)

def look_back_to_center():
    diff_y = constants.DEFAULT_EYE_Y - archi.left_eye.y
    diff_x = constants.DEFAULT_LEFT_EYE_X - archi.left_eye.x
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

    while abs(x) <= constants.LOOK_MOVEMENT_RANGE and abs(y) <= constants.LOOK_MOVEMENT_RANGE:
        render_eyes(
            y1=archi.left_eye.y + y,
            x1=archi.left_eye.x + x,
            y2=archi.left_eye.y + y,
            x2=archi.left_eye.x + x
        )

        x += dx * constants.LOOK_MOVEMENT_STEP
        y += dy * constants.LOOK_MOVEMENT_STEP

        time.sleep(0.001)

def look_around():
    dx1, dy1 = random.choice(list(DIRECTIONS.values()))
    look_to(dx1, dy1)
    time.sleep(1)

    look_back_to_center()

    dx2, dy2 = random.choice(list(DIRECTIONS.values()))
    look_to(dx2, dy2)
    time.sleep(1)

    look_back_to_center()
    time.sleep(1)

def squeeze_eyes_and_back():
    for h in range(constants.DEFAULT_EYE_H, 30, -5):
        render_eyes(height1=h, height2=h)
        time.sleep(0.0001)
    time.sleep(3)
    for h in range(30, constants.DEFAULT_EYE_H, 5):
        render_eyes(height1=h, height2=h)
        time.sleep(0.0001)


def blink_default_eyes():
    for h in range(constants.DEFAULT_EYE_H, 5, -16):
        render_eyes(height1=h, height2=h)
        flush_buffer()
        time.sleep(0.0001)
    for h in range(5, constants.DEFAULT_EYE_H, 16):
        render_eyes(height1=h, height2=h)
        flush_buffer()
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
    for h in range(5, constants.DEFAULT_EYE_H, 3):
        render_eyes(height1=h, height2=h)
        time.sleep(0.001)

    time.sleep(1)
    blink_default_eyes()
    look_around()
    squeeze_eyes_and_back()
    time.sleep(1)
    render_eyes()
    # susface()

LEVITATION_STEP = 1
def levitate_default_single():
    for y in range(archi.left_eye.y, archi.left_eye.y+15, LEVITATION_STEP):
        render_eyes(y1=y, y2=y)
        flush_buffer()
        time.sleep(0.01)

    for y in range(archi.left_eye.y, archi.left_eye.y-15, -LEVITATION_STEP):
        render_eyes(y1=y, y2=y)
        flush_buffer()
        time.sleep(0.01)

    if random.randint(0, 1) == 1:
        blink_default_eyes()

    for y in range(archi.left_eye.y, archi.left_eye.y+15, LEVITATION_STEP):
        render_eyes(y1=y, y2=y)
        flush_buffer()
        time.sleep(0.01)

    for y in range(archi.left_eye.y, archi.left_eye.y-15, -LEVITATION_STEP):
        render_eyes(y1=y, y2=y)
        flush_buffer()
        time.sleep(0.01)

    # def check_button_status(self):
    #     current_state = self.action_button.value()
    #
    #     if self.last_button_state == 1 and current_state == 0:
    #         self.button_clicked += 1
    #         print("Counter:", self.button_clicked)
    #         time.sleep(0.2) 

def default_mood():
    time.sleep(1)
    look_around_reps = random.randrange(1, 3)
    for rep in range(look_around_reps):
        name, (dx, dy) = random.choice(list(DIRECTIONS.items()))
        if name == archi.last_look_action:
            time.sleep(1)
            continue
        archi.last_look_action = name
        look_to(dx, dy)
        time.sleep(1)
        look_back_to_center()
        rep += 1

    levitate_reps = random.randrange(5, 15)
    for rep in range(levitate_reps):
        levitate_default_single()
        rep += 1

    time.sleep(1)


def render_hungry_mouth(drool_height = archi.drool.h):
    # Draw over drool
    fb.fill_rect(0, archi.mouth.y, constants.DISPLAY_W, 60, constants.BLACK)

    # Mouth
    graphics.fill_circle(fb, archi.mouth.x, archi.mouth.y, archi.mouth.r, constants.WHITE)

    # Drool
    archi.drool.h = drool_height
    fb.fill_rect(archi.drool.x, archi.drool.y, archi.drool.w, archi.drool.h, constants.WHITE)

def blink_with_mouth():
    for h in range(constants.DEFAULT_EYE_H, 5, -16):
        render_eyes(height1=h, height2=h)
        render_hungry_mouth()
        flush_buffer()
        time.sleep(0.0001)
    for h in range(5, constants.DEFAULT_EYE_H, 16):
        render_eyes(height1=h, height2=h)
        render_hungry_mouth(archi.drool.h)
        flush_buffer()
        time.sleep(0.0001)
    time.sleep(0.05)

def hungry_mood():
    # blink random
    # drool up and right
    render_eyes()
    render_hungry_mouth()
    flush_buffer()

    while True:
        # longer drool
        if random.randrange(1, 3) == 1:
            for h in range(archi.drool.h, archi.drool.h+15, LEVITATION_STEP):
                render_hungry_mouth(h)
                flush_buffer()
                time.sleep(0.1)

            time.sleep(0.5)
            # small drip of saliva
            drip_pos = archi.drool.y+archi.drool.h
            fb.fill_rect(archi.drool.x, drip_pos, archi.drool.w, 8, constants.WHITE)
            flush_buffer()

            while drip_pos < constants.DISPLAY_H:
                fb.fill_rect(archi.drool.x, drip_pos, archi.drool.w, 8, constants.BLACK)
                fb.fill_rect(archi.drool.x, drip_pos+1, archi.drool.w, 8, constants.WHITE)
                flush_buffer()
                drip_pos += 1
                time.sleep(0.01)

            # shorter drool
            for h in range(archi.drool.h, archi.drool.h-15, -LEVITATION_STEP):
                render_hungry_mouth(h)
                flush_buffer()
                time.sleep(0.01)

        if random.randrange(1, 3) == 1:
            blink_with_mouth()
        else:
            time.sleep(1)

def render_angry_eyes(
        # NOTE: -15 for height
        height1=constants.DEFAULT_EYE_H-15,
        width1=constants.DEFAULT_EYE_W,
        height2=constants.DEFAULT_EYE_H-15,
        width2=constants.DEFAULT_EYE_W,
        x1=45, x2=135, y1 = 0, y2 = 0):
    points_left = [
        (x1, y1),                 # top outer
        (x1 + width1, y1 + 20),        # top inner (lower)
        (x1 + width1, y1 + height1),    # bottom inner
        (x1 + 10, y1 + height1)         # bottom outer
    ]

    fb.fill(0)

    y1 = 120 - height1//2 if y1 == 0 else y1
    y2 = 120 - height2//2 if y2 == 0 else y2
    # left eye
    archi.left_eye.x = x1
    archi.left_eye.y = y1
    archi.left_eye.w = width1
    archi.left_eye.h = height1
    graphics.fill_polygon(fb, points_left, constants.WHITE)

    points_right = [
        (x2, y2 + 20),            # top inner
        (x2 + width2, y2),             # top outer
        (x2 + width2 - 10, y2 + height2),    # bottom outer
        (x2, y2 + height2)         # bottom inner
    ]
    # right eye
    archi.right_eye.x = x2
    archi.right_eye.y = y2
    archi.right_eye.w = width2
    archi.right_eye.h = height2
    graphics.fill_polygon(fb, points_right, constants.WHITE)

def render_sad_eyes(
        # NOTE: -15 for height
        height1=constants.DEFAULT_EYE_H-15,
        width1=constants.DEFAULT_EYE_W,
        height2=constants.DEFAULT_EYE_H-15,
        width2=constants.DEFAULT_EYE_W,
        x1=45, x2=135, y1 = 0, y2 = 0):
    points_left = [
        (x1, y1+25),                 # top outer
        (x1 + width1, y1),        # top inner (lower)
        (x1 + width1, y1 + height1),    # bottom inner
        (x1 + 10, y1 + height1)         # bottom outer
    ]
    fb.fill(0)

    y1 = 120 - height1//2 if y1 == 0 else y1
    y2 = 120 - height2//2 if y2 == 0 else y2

    # left eye
    archi.left_eye.x = x1
    archi.left_eye.y = y1
    archi.left_eye.w = width1
    archi.left_eye.h = height1
    graphics.fill_polygon(fb, points_left, constants.WHITE)

    points_right = [
        (x2, y2),            # top inner
        (x2 + width2, y2+25),             # top outer
        (x2 + width2 - 10, y2 + height2),    # bottom outer
        (x2, y2 + height2)         # bottom inner
    ]
    # right eye
    archi.right_eye.x = x2
    archi.right_eye.y = y2
    archi.right_eye.w = width2
    archi.right_eye.h = height2
    graphics.fill_polygon(fb, points_right, constants.WHITE)


def angry_mood():
    # 1. when annoyed
    # 2. when didnt sleep well
    fb.fill(0)
    flush_buffer()

    # levitate
    while True:
        for y in range(archi.left_eye.y, archi.left_eye.y+15, LEVITATION_STEP):
            render_angry_eyes(y1=y, y2=y)
            flush_buffer()
            time.sleep(0.01)

        for y in range(archi.left_eye.y, archi.left_eye.y-15, -LEVITATION_STEP):
            render_angry_eyes(y1=y, y2=y)
            flush_buffer()
            time.sleep(0.01)

        for y in range(archi.left_eye.y, archi.left_eye.y+15, LEVITATION_STEP):
            render_angry_eyes(y1=y, y2=y)
            flush_buffer()
            time.sleep(0.01)

        for y in range(archi.left_eye.y, archi.left_eye.y-15, -LEVITATION_STEP):
            render_angry_eyes(y1=y, y2=y)
            flush_buffer()
            time.sleep(0.01)

def sad_mood():
    fb.fill(0)
    flush_buffer()
    # levitate
    while True:
        for y in range(archi.left_eye.y, archi.left_eye.y+15, LEVITATION_STEP):
            render_sad_eyes(y1=y, y2=y)
            flush_buffer()
            time.sleep(0.01)

        for y in range(archi.left_eye.y, archi.left_eye.y-15, -LEVITATION_STEP):
            render_sad_eyes(y1=y, y2=y)
            flush_buffer()
            time.sleep(0.01)

        for y in range(archi.left_eye.y, archi.left_eye.y+15, LEVITATION_STEP):
            render_sad_eyes(y1=y, y2=y)
            flush_buffer()
            time.sleep(0.01)

        for y in range(archi.left_eye.y, archi.left_eye.y-15, -LEVITATION_STEP):
            render_sad_eyes(y1=y, y2=y)
            flush_buffer()
            time.sleep(0.01)

def sus_mood():
    for h in range(archi.left_eye.h, 30, -5):
        render_eyes(height1=h)
        time.sleep(0.0001)

def sleeping_mood():
    #   1. specific time of a day
    #   2. after food
    #   3. can be woken up
    #   4. count down the tiredness
    #   5. if tiredness => 50 then angry face
    print("I'm sleeping")

def tired_mood():
    print("I'm tired")

def pick_compliment():
    fb.fill(0)
    flush_buffer()
    texts = [
            ["You look",  "beautiful", "today :)"],
            ["You look",  "cute", "today"],
            ["You are", "so so", "gorgeous"],
            ["Your smile", "brings", "happines"],
            ["You have", "amazing", "smile"],
            ["You have", "beautiful", "eyes"]
    ]
    lines = random.choice(texts)
    text_renderer.render_three_text_lines_center(tft, lines[0], lines[1], lines[2], constants.WHITE)

def loving_mood():
    # render_hearts()

    # if arch.hungry > 60 - only then the loving mode 
    # if happy -> show curved eyes
    # if pressed once -> light squise eyes 
    # if pressed twice -> more squise eyes 
    # if pressed three time -> 
        # open eyes
        # show hearts
        # show text -> pick_compliment
    print("I'm in love")


def button_pressed(pin):
    time.sleep(0.2)
    # TODO: WHEN TO MAKE IT 0
    archi.button_clicked += 1
    print("Button pressed types:", archi.button_clicked)
    # if archi.mood == arch.Mood.DEFAULT:
    #     archi.mood = arch.Mood.HUNGRY
    # else:
    #     archi.mood = arch.Mood.DEFAULT

button = Pin(19, Pin.IN, Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed)

def happy_birthday():
    t = time.localtime()
    # 22.04
    month = t[1]
    day   = t[2]

    if month == 4 and day == 22:
        print("Happy birthday, Ecenur!")

def main():
    fb.fill(0)
    flush_buffer()

    # TODO: Implement check of happy_birthday on each mood

    # boot()
    # booting_eyes()
    # greeting()
    # render_eyes()
    # flush_buffer()
    # hungry_mood()
    angry_mood()
    # sad_mood()
    # while True:
    #     if archi.mood == Mood.DEFAULT:
    #         default_mood()
# TODO: happy birthday 

# ============= DO NOT TOUCH ME OR YOU WILL REGRET LATER =============
main()
