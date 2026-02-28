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

def render_eyes(
        height1=constants.DEFAULT_EYE_H,
        width1=constants.DEFAULT_EYE_W,
        height2=constants.DEFAULT_EYE_H,
        width2=constants.DEFAULT_EYE_W,
        x1=constants.DEFAULT_LEFT_EYE_X,
        x2=constants.DEFAULT_RIGHT_EYE_X, 
        y1 = 0, y2 = 0
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

def render_loving_eyes(size = 70):
    fb.fill(0)

    archi.left_eye.y = constants.DEFAULT_LOVING_Y
    graphics.draw_heart(fb, 75, archi.left_eye.y, size, constants.WHITE)

    archi.right_eye.y = constants.DEFAULT_LOVING_Y
    graphics.draw_heart(fb, 165, archi.right_eye.y, size, constants.WHITE)

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

def look_to(dx, dy, timeout = 0.001):
    x = 0
    y = 0

    while abs(x) <= constants.LOOK_MOVEMENT_RANGE and abs(y) <= constants.LOOK_MOVEMENT_RANGE:
        render_eyes(
            y1=archi.left_eye.y + y,
            x1=archi.left_eye.x + x,
            y2=archi.right_eye.y + y,
            x2=archi.right_eye.x + x
        )
        flush_buffer()

        x += dx * constants.LOOK_MOVEMENT_STEP
        y += dy * constants.LOOK_MOVEMENT_STEP

        time.sleep(timeout)

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

LEVITATION_STEP = 1
def levitate_default_single(timeout = 0.01):
    for y in range(archi.left_eye.y, archi.left_eye.y+15, LEVITATION_STEP):
        render_eyes(y1=y, y2=y)
        flush_buffer()
        time.sleep(timeout)

    for y in range(archi.left_eye.y, archi.left_eye.y-15, -LEVITATION_STEP):
        render_eyes(y1=y, y2=y)
        flush_buffer()
        time.sleep(timeout)

    if random.randint(0, 1) == 1:
        blink_default_eyes()

    for y in range(archi.left_eye.y, archi.left_eye.y+15, LEVITATION_STEP):
        render_eyes(y1=y, y2=y)
        flush_buffer()
        time.sleep(timeout)

    for y in range(archi.left_eye.y, archi.left_eye.y-15, -LEVITATION_STEP):
        render_eyes(y1=y, y2=y)
        flush_buffer()
        time.sleep(timeout)

def switch_mood():
    new_mood = archi.mood
    if new_mood == arch.MOOD.SUS:
        sus_mood()

    if new_mood == arch.MOOD.LOVING:
        loving_mood()

def default_mood():
    render_eyes()
    flush_buffer()
    while archi.mood == arch.MOOD.DEFAULT:
        if archi.should_switch_mod(arch.MOOD.DEFAULT):
            break

        levitate_reps = random.randrange(5, 15)
        for rep in range(levitate_reps):
            if archi.should_switch_mod(arch.MOOD.DEFAULT):
                break
            levitate_default_single()
            rep += 1

        look_around_reps = random.randrange(1, 2)
        for rep in range(look_around_reps):
            name, (dx, dy) = random.choice(list(DIRECTIONS.items()))
            if archi.should_switch_mod(arch.MOOD.DEFAULT):
                break
            if name == archi.last_look_action:
                time.sleep(1)
                continue
            archi.last_look_action = name
            look_to(dx, dy)
            time.sleep(1)
            look_back_to_center()
            rep += 1

        time.sleep(1)
    switch_mood()


def render_hungry_mouth(drool_height = archi.drool.h):
    # Draw over drool
    fb.fill_rect(0, archi.mouth.y, constants.DISPLAY_W, 60, constants.BLACK)

    # Mouth
    graphics.fill_circle(fb, archi.mouth.x, archi.mouth.y, archi.mouth.r, constants.WHITE)

    # Drool
    archi.drool.h = drool_height
    fb.fill_rect(archi.drool.x, archi.drool.y, archi.drool.w, archi.drool.h, constants.WHITE)

def render_default_mouth(y=archi.mouth.y, r=archi.mouth.r):
    archi.mouth.r = r
    graphics.fill_circle(fb, archi.mouth.x, y, archi.mouth.r, constants.WHITE)

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
    render_eyes()
    render_hungry_mouth()
    flush_buffer()

    while archi.mood == arch.MOOD.HUNGRY:
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
        x1=constants.DEFAULT_LEFT_EYE_X,
        x2=constants.DEFAULT_RIGHT_EYE_X, 
        y1 = 0, y2 = 0):
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
        x1=constants.DEFAULT_LEFT_EYE_X,
        x2=constants.DEFAULT_RIGHT_EYE_X, 
        y1 = 0, y2 = 0):
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
    while archi.mood == arch.MOOD.ANGRY:
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
    while archi.mood == arch.MOOD.SAD:
        for y in range(archi.left_eye.y, archi.left_eye.y+15, LEVITATION_STEP):
            if archi.should_switch_mod(arch.MOOD.SAD):
                break
            render_sad_eyes(y1=y, y2=y)
            flush_buffer()
            time.sleep(0.01)

        for y in range(archi.left_eye.y, archi.left_eye.y-15, -LEVITATION_STEP):
            if archi.should_switch_mod(arch.MOOD.SAD):
                break
            render_sad_eyes(y1=y, y2=y)
            flush_buffer()
            time.sleep(0.01)

        for y in range(archi.left_eye.y, archi.left_eye.y+15, LEVITATION_STEP):
            if archi.should_switch_mod(arch.MOOD.SAD):
                break
            render_sad_eyes(y1=y, y2=y)
            flush_buffer()
            time.sleep(0.01)

        for y in range(archi.left_eye.y, archi.left_eye.y-15, -LEVITATION_STEP):
            if archi.should_switch_mod(arch.MOOD.SAD):
                break
            render_sad_eyes(y1=y, y2=y)
            flush_buffer()
            time.sleep(0.01)

def sus_mood():
    while archi.mood == arch.MOOD.SUS:
        archi.should_switch_mod(arch.MOOD.SUS)
        for h in range(archi.left_eye.h, 30, -5):
            if archi.should_switch_mod(arch.MOOD.SUS):
                break
            render_eyes(height1=h, height2=h)
            flush_buffer()
            time.sleep(0.0001)

        time.sleep(3)

        for h in range(archi.left_eye.h, 65, 5):
            if archi.should_switch_mod(arch.MOOD.SUS):
                break
            render_eyes(height1=h, height2=h)
            flush_buffer()
            time.sleep(0.0001)
        time.sleep(3)
    switch_mood()

def sleeping_mood():
    for h in range(archi.left_eye.h, 5, -1):
        render_eyes(height1=h, height2=h)
        flush_buffer()
        time.sleep(0.0001)
    while archi.mood == arch.MOOD.SLEEPING:
        for r in range(archi.mouth.r, 23, 1):
            if archi.should_switch_mod(arch.MOOD.SLEEPING):
                break
            render_eyes(height1=archi.left_eye.h, height2=archi.right_eye.h)
            render_default_mouth(r=r)
            flush_buffer()
            time.sleep(0.01)

        time.sleep(0.5)

        for r in range(archi.mouth.r, 0, -1):
            if archi.should_switch_mod(arch.MOOD.SLEEPING):
                break
            render_eyes(height1=archi.left_eye.h, height2=archi.right_eye.h)
            render_default_mouth(r=r)
            flush_buffer()
            time.sleep(0.01)
        time.sleep(2.5)
    switch_mood()

def tired_mood():
    # SLOWLY squise eys
    # FAST open it
    # randomly SLOW look around
    # no levitaion

    # archi.should_switch_mod(arch.MOOD.TIRED)
    render_eyes()
    flush_buffer()
    while archi.mood == arch.MOOD.TIRED:
        if archi.should_switch_mod(arch.MOOD.TIRED):
            break
        if random.randrange(1, 5) == 1:
            for h in range(archi.left_eye.h, 5, -1):
                if archi.should_switch_mod(arch.MOOD.TIRED):
                    break
                render_eyes(height1=h, height2=h)
                flush_buffer()
                time.sleep(0.0001)

            time.sleep(1)

            for r in range(archi.mouth.r, 23, 1):
                if archi.should_switch_mod(arch.MOOD.TIRED):
                    break
                # render_eyes(height1=5, height2=5)
                render_eyes(height1=archi.left_eye.h, height2=archi.right_eye.h)
                render_default_mouth(r=r)
                flush_buffer()
                time.sleep(0.01)

            time.sleep(1)

            for r in range(archi.mouth.r, 0, -1):
                if archi.should_switch_mod(arch.MOOD.TIRED):
                    break
                render_eyes(height1=archi.left_eye.h, height2=archi.right_eye.h)
                # render_eyes(height1=5, height2=5)
                render_default_mouth(r=r)
                flush_buffer()
                time.sleep(0.01)

            time.sleep(1)
                
            for h in range(archi.left_eye.h, constants.DEFAULT_EYE_H, 5):
                if archi.should_switch_mod(arch.MOOD.TIRED):
                    break
                render_eyes(height1=h, height2=h)
                flush_buffer()
                time.sleep(0.0001)
            time.sleep(1)

        if random.randrange(1, 3) == 1:
            for h in range(archi.left_eye.h, 5, -1):
                if archi.should_switch_mod(arch.MOOD.TIRED):
                    break
                render_eyes(height1=h, height2=h)
                flush_buffer()
                time.sleep(0.0001)

            time.sleep(3)

            for h in range(archi.left_eye.h, constants.DEFAULT_EYE_H, 5):
                if archi.should_switch_mod(arch.MOOD.TIRED):
                    break
                render_eyes(height1=h, height2=h)
                flush_buffer()
                time.sleep(0.0001)
            time.sleep(1)

        levitation_steps = random.randrange(1, 6)
        # levitate
        for step in range(levitation_steps):
            for y in range(archi.left_eye.y, archi.left_eye.y+15, LEVITATION_STEP):
                if archi.should_switch_mod(arch.MOOD.TIRED):
                    break
                render_eyes(y1=y, y2=y)
                flush_buffer()
                time.sleep(0.01)

            for y in range(archi.left_eye.y, archi.left_eye.y-15, -LEVITATION_STEP):
                if archi.should_switch_mod(arch.MOOD.TIRED):
                    break
                render_eyes(y1=y, y2=y)
                flush_buffer()
                time.sleep(0.01)

            for y in range(archi.left_eye.y, archi.left_eye.y+15, LEVITATION_STEP):
                if archi.should_switch_mod(arch.MOOD.TIRED):
                    break
                render_eyes(y1=y, y2=y)
                flush_buffer()
                time.sleep(0.01)

            for y in range(archi.left_eye.y, archi.left_eye.y-15, -LEVITATION_STEP):
                if archi.should_switch_mod(arch.MOOD.TIRED):
                    break
                render_eyes(y1=y, y2=y)
                flush_buffer()
                time.sleep(0.01)

            step += 1
        time.sleep(1)

    switch_mood()

def pick_compliment():
    fb.fill(0)
    flush_buffer()
    texts = [
            ["You look",  "beautiful", "today :)"],
            ["You look",  "cute", "today"],
            ["You are", "so so", "gorgeous"],
            ["Your smile", "brings", "happines"],
            ["You have", "beautiful", "eyes"],
            ["You are", "the best", ":)"],
            ["You are", "loved", ""],
            ["You are", "valued", ""],
            ["I'm", "proud", "of you"],
            ["You", "bring", "peace"],
            ["You", "feel", "like home"],
            ["I love", "your", "smell"]
    ]
    lines = random.choice(texts)
    text_renderer.render_three_text_lines_center(tft, lines[0], lines[1], lines[2], constants.WHITE)

def should_show_compliment():
    if (archi.loving_compliment):
        pick_compliment()
        time.sleep(2)
        archi.loving_compliment = False

def loving_mood():
    while archi.mood == arch.MOOD.LOVING:
        for size in range(70, 80, 5):
            should_show_compliment()
            if archi.should_switch_mod(arch.MOOD.LOVING):
                break

            render_loving_eyes(size)
            render_default_mouth()
            flush_buffer()
            time.sleep(0.005)

        for size in range(80, 70, -5):
            should_show_compliment()
            if archi.should_switch_mod(arch.MOOD.LOVING):
                break

            render_loving_eyes(size)
            render_default_mouth()
            flush_buffer()
            time.sleep(0.005)

    switch_mood()

    # if arch.hungry > 60 - only then the loving mode 
    # if happy -> show curved eyes
    # if pressed once -> light squise eyes 
    # if pressed twice -> more squise eyes 
    # if pressed three time -> 
        # open eyes
        # show hearts
        # show text -> pick_compliment

def eating_mood():
    for h in range(archi.left_eye.h, 25, -1):
        render_eyes(height1=h, height2=h)
        flush_buffer()
        time.sleep(0.0001)
    while True:
        for i in range(10):
            for w in range(36, 48, 2):
                fb.fill(0)
                render_eyes(height1=archi.left_eye.h, height2=archi.right_eye.h)
                # render_eyes(height1=25, height2=25)
                x_mouth = 125 - w // 2
                fb.fill_rect(x_mouth-8, 160, 3, 20, constants.WHITE)
                fb.fill_rect(x_mouth, 165, w, 8, constants.WHITE)
                fb.fill_rect(x_mouth+w+5, 160, 3, 20, constants.WHITE)

                flush_buffer()
                time.sleep(0.02)

            for w in range(48, 36, -2):
                fb.fill(0)
                render_eyes(height1=archi.left_eye.h, height2=archi.right_eye.h)
                # render_eyes(height1=25, height2=25)
                x_mouth = 125 - w // 2
                fb.fill_rect(x_mouth-8, 160, 3, 20, constants.WHITE)
                fb.fill_rect(x_mouth, 165, w, 8, constants.WHITE)
                fb.fill_rect(x_mouth+w+5, 160, 3, 20, constants.WHITE)

                flush_buffer()
                time.sleep(0.02)
            i +=1

        # REMOVE ME
        time.sleep(3)
        # REMOVE ME

    # archi.mood = arch.MOOD.DEFAULT

def waking_up_mood():
    print("waking up")

last_press_time = 0
def button_pressed(pin):
    global last_press_time

    current_time = time.ticks_ms()

    if time.ticks_diff(current_time, last_press_time) > 200:
        last_press_time = current_time
        # IGNORE IF SPECIFIC MODE IS ENABLED
        if archi.mood == arch.MOOD.EATING or archi.mood == arch.MOOD.WAKING_UP:
            return

        archi.button_clicked += 1

        if archi.button_clicked == 1 and archi.mood == arch.MOOD.DEFAULT:
            archi.mood = arch.MOOD.SUS

        if archi.button_clicked == 2 and archi.mood == arch.MOOD.SUS:
            archi.mood = arch.MOOD.LOVING

        # if archi.mode == arch.MOOD.LOVING:
        #     archi.loving_compliment = True

        print("Button pressed times:", archi.button_clicked)

button = Pin(19, Pin.IN, Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed)

def happy_birthday():
    t = time.localtime()
    # 22.04
    month = t[1]
    day   = t[2]

    if month == 4 and day == 22:
        print("Happy birthday, Ecenur!")

def render_mood():
    if archi.mood == arch.MOOD.DEFAULT:
        default_mood()
    elif archi.mood == arch.MOOD.HUNGRY:
        hungry_mood()
    elif archi.mood == arch.MOOD.SLEEPING:
        sleeping_mood()
    elif archi.mood == arch.MOOD.WAKING_UP:
        waking_up_mood()
    elif archi.mood == arch.MOOD.ANGRY:
        angry_mood()
    elif archi.mood == arch.MOOD.TIRED:
        tired_mood()
    elif archi.mood == arch.MOOD.SAD:
        sad_mood()
    elif archi.mood == arch.MOOD.LOVING:
        loving_mood()
    elif archi.mood == arch.MOOD.SUS:
        sus_mood()
    elif archi.mood == arch.MOOD.EATING:
        eating_mood()

def main():
    fb.fill(0)
    flush_buffer()
    # boot()
    # booting_eyes()
    # greeting()
    archi.mood = arch.MOOD.EATING
    while True:
        render_mood()
    # TODO: Implement check of happy_birthday on each mode

# TODO: happy birthday 

main()
