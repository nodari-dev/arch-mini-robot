from machine import Pin, SPI
import framebuf
import random
import time
import math
from lib import st7789py as st7789
from lib import text_renderer
from lib import arch as archlib
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
    time.sleep(1)
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


arch = archlib.Archi()

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
    arch.left_eye.x = x1
    arch.left_eye.y = y1
    arch.left_eye.w = width1
    arch.left_eye.h = height1
    graphics.draw_eye(fb, x1, y1, width1, height1, 10, constants.WHITE)

    # right eye
    arch.right_eye.x = x2
    arch.right_eye.y = y2
    arch.right_eye.w = width2
    arch.right_eye.h = height2
    graphics.draw_eye(fb, x2, y2, width2, height2, 10, constants.WHITE)

    # tft.blit_buffer(buffer, 0, 0, constants.DISPLAY_W, constants.DISPLAY_H)

def render_loving_eyes(size = 70):
    fb.fill(0)

    arch.left_eye.y = constants.DEFAULT_LOVING_Y
    graphics.draw_heart(fb, 75, arch.left_eye.y, size, constants.WHITE)

    arch.right_eye.y = constants.DEFAULT_LOVING_Y
    graphics.draw_heart(fb, 165, arch.right_eye.y, size, constants.WHITE)

def sign(value):
    return (value > 0) - (value < 0)

def look_back_to_center():
    diff_y = constants.DEFAULT_EYE_Y - arch.left_eye.y
    diff_x = constants.DEFAULT_LEFT_EYE_X - arch.left_eye.x
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
            y1=arch.left_eye.y + y,
            x1=arch.left_eye.x + x,
            y2=arch.right_eye.y + y,
            x2=arch.right_eye.x + x
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
    flush_buffer()
    time.sleep(1)

    # try to open eyes
    for h in range(5, 20, 1):
        render_eyes(height1=h, height2=h)
        flush_buffer()
        time.sleep(0.001)

    for h in range(20, 5, -1):
        render_eyes(height1=h, height2=h)
        flush_buffer()
        time.sleep(0.001)

    time.sleep(1)

    for h in range(5, 20, 1):
        render_eyes(height1=h, height2=h)
        flush_buffer()
        time.sleep(0.001)
    time.sleep(1)

    for h in range(20, 5, -1):
        render_eyes(height1=h, height2=h)
        flush_buffer()
        time.sleep(0.001)

    time.sleep(2.5)

    # Open eyes fully
    for h in range(5, constants.DEFAULT_EYE_H, 3):
        render_eyes(height1=h, height2=h)
        flush_buffer()
        time.sleep(0.001)

    time.sleep(1)
    blink_default_eyes()
    look_around()
    for h in range(constants.DEFAULT_EYE_H, 30, -5):
        render_eyes(height1=h, height2=h)
        time.sleep(0.0001)
    time.sleep(3)
    for h in range(30, constants.DEFAULT_EYE_H, 5):
        render_eyes(height1=h, height2=h)
        time.sleep(0.0001)
    time.sleep(1)
    render_eyes()
    flush_buffer()

LEVITATION_STEP = 1
def levitate_default_single(timeout = 0.01):
    for y in range(arch.left_eye.y, arch.left_eye.y+15, LEVITATION_STEP):
        render_eyes(y1=y, y2=y)
        flush_buffer()
        time.sleep(timeout)

    for y in range(arch.left_eye.y, arch.left_eye.y-15, -LEVITATION_STEP):
        render_eyes(y1=y, y2=y)
        flush_buffer()
        time.sleep(timeout)

    if random.randint(0, 1) == 1:
        blink_default_eyes()

    for y in range(arch.left_eye.y, arch.left_eye.y+15, LEVITATION_STEP):
        render_eyes(y1=y, y2=y)
        flush_buffer()
        time.sleep(timeout)

    for y in range(arch.left_eye.y, arch.left_eye.y-15, -LEVITATION_STEP):
        render_eyes(y1=y, y2=y)
        flush_buffer()
        time.sleep(timeout)

def default_mood():
    render_eyes()
    flush_buffer()
    while arch.mood == archlib.MOOD.DEFAULT:
        if arch.should_switch_mod(archlib.MOOD.DEFAULT):
            break

        levitate_reps = random.randrange(5, 15)
        for rep in range(levitate_reps):
            if arch.should_switch_mod(archlib.MOOD.DEFAULT):
                break
            levitate_default_single()
            rep += 1

        look_around_reps = random.randrange(1, 2)
        for rep in range(look_around_reps):
            name, (dx, dy) = random.choice(list(DIRECTIONS.items()))
            if arch.should_switch_mod(archlib.MOOD.DEFAULT):
                break
            if name == arch.last_look_action:
                time.sleep(1)
                continue
            arch.last_look_action = name
            look_to(dx, dy)
            time.sleep(1)
            look_back_to_center()
            rep += 1

        time.sleep(1)
    render_mood()

def render_hungry_mouth(drool_height = arch.drool.h):
    # Draw over drool
    fb.fill_rect(0, arch.mouth.y, constants.DISPLAY_W, 60, constants.BLACK)

    # Mouth
    graphics.fill_circle(fb, arch.mouth.x, arch.mouth.y, arch.mouth.r, constants.WHITE)

    # Drool
    arch.drool.h = drool_height
    fb.fill_rect(arch.drool.x, arch.drool.y, arch.drool.w, arch.drool.h, constants.WHITE)

def render_default_mouth(y=arch.mouth.y, r=arch.mouth.r):
    arch.mouth.r = r
    graphics.fill_circle(fb, arch.mouth.x, y, arch.mouth.r, constants.WHITE)

def blink_with_mouth():
    for h in range(constants.DEFAULT_EYE_H, 5, -16):
        render_eyes(height1=h, height2=h)
        render_hungry_mouth()
        flush_buffer()
        time.sleep(0.0001)
    for h in range(5, constants.DEFAULT_EYE_H, 16):
        render_eyes(height1=h, height2=h)
        render_hungry_mouth(arch.drool.h)
        flush_buffer()
        time.sleep(0.0001)
    time.sleep(0.05)

def hungry_mood():
    render_eyes()
    render_hungry_mouth()
    flush_buffer()

    while arch.mood == archlib.MOOD.HUNGRY:
        # longer drool
        if random.randrange(1, 3) == 1:
            for h in range(arch.drool.h, arch.drool.h+15, LEVITATION_STEP):
                render_hungry_mouth(h)
                flush_buffer()
                time.sleep(0.1)

            time.sleep(0.5)
            # small drip of saliva
            drip_pos = arch.drool.y+arch.drool.h
            fb.fill_rect(arch.drool.x, drip_pos, arch.drool.w, 8, constants.WHITE)
            flush_buffer()

            while drip_pos < constants.DISPLAY_H:
                fb.fill_rect(arch.drool.x, drip_pos, arch.drool.w, 8, constants.BLACK)
                fb.fill_rect(arch.drool.x, drip_pos+1, arch.drool.w, 8, constants.WHITE)
                flush_buffer()
                drip_pos += 1
                time.sleep(0.01)

            # shorter drool
            for h in range(arch.drool.h, arch.drool.h-15, -LEVITATION_STEP):
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
    arch.left_eye.x = x1
    arch.left_eye.y = y1
    arch.left_eye.w = width1
    arch.left_eye.h = height1
    graphics.fill_polygon(fb, points_left, constants.WHITE)

    points_right = [
        (x2, y2 + 20),            # top inner
        (x2 + width2, y2),             # top outer
        (x2 + width2 - 10, y2 + height2),    # bottom outer
        (x2, y2 + height2)         # bottom inner
    ]
    # right eye
    arch.right_eye.x = x2
    arch.right_eye.y = y2
    arch.right_eye.w = width2
    arch.right_eye.h = height2
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
    arch.left_eye.x = x1
    arch.left_eye.y = y1
    arch.left_eye.w = width1
    arch.left_eye.h = height1
    graphics.fill_polygon(fb, points_left, constants.WHITE)

    points_right = [
        (x2, y2),            # top inner
        (x2 + width2, y2+25),             # top outer
        (x2 + width2 - 10, y2 + height2),    # bottom outer
        (x2, y2 + height2)         # bottom inner
    ]
    # right eye
    arch.right_eye.x = x2
    arch.right_eye.y = y2
    arch.right_eye.w = width2
    arch.right_eye.h = height2
    graphics.fill_polygon(fb, points_right, constants.WHITE)


def angry_mood():
    # 1. when annoyed
    # 2. when didnt sleep well
    fb.fill(0)
    flush_buffer()

    # levitate
    while arch.mood == archlib.MOOD.ANGRY:
        for y in range(arch.left_eye.y, arch.left_eye.y+15, LEVITATION_STEP):
            render_angry_eyes(y1=y, y2=y)
            flush_buffer()
            time.sleep(0.01)

        for y in range(arch.left_eye.y, arch.left_eye.y-15, -LEVITATION_STEP):
            render_angry_eyes(y1=y, y2=y)
            flush_buffer()
            time.sleep(0.01)

        for y in range(arch.left_eye.y, arch.left_eye.y+15, LEVITATION_STEP):
            render_angry_eyes(y1=y, y2=y)
            flush_buffer()
            time.sleep(0.01)

        for y in range(arch.left_eye.y, arch.left_eye.y-15, -LEVITATION_STEP):
            render_angry_eyes(y1=y, y2=y)
            flush_buffer()
            time.sleep(0.01)

def sad_mood():
    fb.fill(0)
    flush_buffer()
    # levitate
    while arch.mood == archlib.MOOD.SAD:
        for y in range(arch.left_eye.y, arch.left_eye.y+15, LEVITATION_STEP):
            if arch.should_switch_mod(archlib.MOOD.SAD):
                break
            render_sad_eyes(y1=y, y2=y)
            flush_buffer()
            time.sleep(0.01)

        for y in range(arch.left_eye.y, arch.left_eye.y-15, -LEVITATION_STEP):
            if arch.should_switch_mod(archlib.MOOD.SAD):
                break
            render_sad_eyes(y1=y, y2=y)
            flush_buffer()
            time.sleep(0.01)

        for y in range(arch.left_eye.y, arch.left_eye.y+15, LEVITATION_STEP):
            if arch.should_switch_mod(archlib.MOOD.SAD):
                break
            render_sad_eyes(y1=y, y2=y)
            flush_buffer()
            time.sleep(0.01)

        for y in range(arch.left_eye.y, arch.left_eye.y-15, -LEVITATION_STEP):
            if arch.should_switch_mod(archlib.MOOD.SAD):
                break
            render_sad_eyes(y1=y, y2=y)
            flush_buffer()
            time.sleep(0.01)

def sus_mood():
    while arch.mood == archlib.MOOD.SUS:
        arch.should_switch_mod(archlib.MOOD.SUS)
        for h in range(arch.left_eye.h, 30, -5):
            if arch.should_switch_mod(archlib.MOOD.SUS):
                break
            render_eyes(height1=h, height2=h)
            flush_buffer()
            time.sleep(0.0001)

        time.sleep(3)

        for h in range(arch.left_eye.h, 65, 5):
            if arch.should_switch_mod(archlib.MOOD.SUS):
                break
            render_eyes(height1=h, height2=h)
            flush_buffer()
            time.sleep(0.0001)
        time.sleep(3)
    render_mood()

def sleeping_mood():
    for h in range(arch.left_eye.h, 5, -1):
        render_eyes(height1=h, height2=h)
        flush_buffer()
        time.sleep(0.0001)
    while arch.mood == archlib.MOOD.SLEEPING:
        for r in range(arch.mouth.r, 23, 1):
            if arch.should_switch_mod(archlib.MOOD.SLEEPING):
                break
            render_eyes(height1=arch.left_eye.h, height2=arch.right_eye.h)
            render_default_mouth(r=r)
            flush_buffer()
            time.sleep(0.01)

        time.sleep(0.5)

        for r in range(arch.mouth.r, 0, -1):
            if arch.should_switch_mod(archlib.MOOD.SLEEPING):
                break
            render_eyes(height1=arch.left_eye.h, height2=arch.right_eye.h)
            render_default_mouth(r=r)
            flush_buffer()
            time.sleep(0.01)
        time.sleep(2.5)
    render_mood()

def tired_mood():
    # SLOWLY squise eys
    # FAST open it
    # randomly SLOW look around
    # no levitaion

    render_eyes()
    flush_buffer()
    while arch.mood == archlib.MOOD.TIRED:
        if arch.should_switch_mod(archlib.MOOD.TIRED):
            break
        if random.randrange(1, 5) == 1:
            for h in range(arch.left_eye.h, 5, -1):
                if arch.should_switch_mod(archlib.MOOD.TIRED):
                    break
                render_eyes(height1=h, height2=h)
                flush_buffer()
                time.sleep(0.0001)

            time.sleep(1)

            for r in range(arch.mouth.r, 23, 1):
                if arch.should_switch_mod(archlib.MOOD.TIRED):
                    break
                render_eyes(height1=arch.left_eye.h, height2=arch.right_eye.h)
                render_default_mouth(r=r)
                flush_buffer()
                time.sleep(0.01)

            time.sleep(1)

            for r in range(arch.mouth.r, 0, -1):
                if arch.should_switch_mod(archlib.MOOD.TIRED):
                    break
                render_eyes(height1=arch.left_eye.h, height2=arch.right_eye.h)
                render_default_mouth(r=r)
                flush_buffer()
                time.sleep(0.01)

            time.sleep(1)
                
            for h in range(arch.left_eye.h, constants.DEFAULT_EYE_H, 5):
                if arch.should_switch_mod(archlib.MOOD.TIRED):
                    break
                render_eyes(height1=h, height2=h)
                flush_buffer()
                time.sleep(0.0001)
            time.sleep(1)

        if random.randrange(1, 3) == 1:
            for h in range(arch.left_eye.h, 5, -1):
                if arch.should_switch_mod(archlib.MOOD.TIRED):
                    break
                render_eyes(height1=h, height2=h)
                flush_buffer()
                time.sleep(0.0001)

            time.sleep(3)

            for h in range(arch.left_eye.h, constants.DEFAULT_EYE_H, 5):
                if arch.should_switch_mod(archlib.MOOD.TIRED):
                    break
                render_eyes(height1=h, height2=h)
                flush_buffer()
                time.sleep(0.0001)
            time.sleep(1)

        levitation_steps = random.randrange(1, 6)
        # levitate
        for step in range(levitation_steps):
            for y in range(arch.left_eye.y, arch.left_eye.y+15, LEVITATION_STEP):
                if arch.should_switch_mod(archlib.MOOD.TIRED):
                    break
                render_eyes(y1=y, y2=y)
                flush_buffer()
                time.sleep(0.01)

            for y in range(arch.left_eye.y, arch.left_eye.y-15, -LEVITATION_STEP):
                if arch.should_switch_mod(archlib.MOOD.TIRED):
                    break
                render_eyes(y1=y, y2=y)
                flush_buffer()
                time.sleep(0.01)

            for y in range(arch.left_eye.y, arch.left_eye.y+15, LEVITATION_STEP):
                if arch.should_switch_mod(archlib.MOOD.TIRED):
                    break
                render_eyes(y1=y, y2=y)
                flush_buffer()
                time.sleep(0.01)

            for y in range(arch.left_eye.y, arch.left_eye.y-15, -LEVITATION_STEP):
                if arch.should_switch_mod(archlib.MOOD.TIRED):
                    break
                render_eyes(y1=y, y2=y)
                flush_buffer()
                time.sleep(0.01)

            step += 1
        time.sleep(1)

    render_mood()

def pick_compliment():
    fb.fill(0)
    flush_buffer()
    lines = random.choice(constants.COMPLIMENTS)
    text_renderer.render_three_text_lines_center(tft, lines[0], lines[1], lines[2], constants.WHITE)

def should_show_compliment():
    if (arch.loving_compliment):
        pick_compliment()
        time.sleep(2)
        arch.loving_compliment = False

def loving_mood():
    mood_start_time = time.ticks_ms()
    while arch.mood == archlib.MOOD.LOVING and not arch.time_for_mood_expired(mood_start_time):
        for size in range(70, 80, 5):
            should_show_compliment()
            if arch.should_switch_mod(archlib.MOOD.LOVING):
                break

            render_loving_eyes(size)
            render_default_mouth()
            flush_buffer()
            time.sleep(0.005)

        for size in range(80, 70, -5):
            should_show_compliment()
            if arch.should_switch_mod(archlib.MOOD.LOVING):
                break

            render_loving_eyes(size)
            render_default_mouth()
            flush_buffer()
            time.sleep(0.005)

    arch.mood = archlib.MOOD.DEFAULT
    render_mood()

def eating_mood():
    for h in range(arch.left_eye.h, 25, -1):
        render_eyes(height1=h, height2=h)
        flush_buffer()
        time.sleep(0.0001)


    test = 0
    mood_start_time = time.ticks_ms()
    while True:
    # while archlibi.mood == archlib.MOOD.EATING and not archlibi.time_for_mood_expired(mood_start_time):
        for i in range(10):
            for w in range(36, 48, 2):
                fb.fill(0)
                render_eyes(height1=arch.left_eye.h, height2=arch.right_eye.h)
                x_mouth = 125 - w // 2
                fb.fill_rect(x_mouth-8, 160, 3, 20, constants.WHITE)
                fb.fill_rect(x_mouth, 165, w, 8, constants.WHITE)
                fb.fill_rect(x_mouth+w+5, 160, 3, 20, constants.WHITE)

                flush_buffer()
                time.sleep(0.02)

            for w in range(48, 36, -2):
                fb.fill(0)
                render_eyes(height1=arch.left_eye.h, height2=arch.right_eye.h)
                x_mouth = 125 - w // 2
                fb.fill_rect(x_mouth-8, 160, 3, 20, constants.WHITE)
                fb.fill_rect(x_mouth, 165, w, 8, constants.WHITE)
                fb.fill_rect(x_mouth+w+5, 160, 3, 20, constants.WHITE)

                flush_buffer()
                time.sleep(0.02)
            i +=1
            test +=1
            if test == 8:
                break

        if test == 8:
            break

    arch.mood = archlib.MOOD.DEFAULT
    render_mood()

def waking_up_mood():
    print("waking up")

last_press_time = 0
def button_pressed(pin):
    global last_press_time

    current_time = time.ticks_ms()
    print(arch.mood)

    if time.ticks_diff(current_time, last_press_time) > 200:
        last_press_time = current_time
        # IGNORE IF SPECIFIC MODE IS ENABLED
        if (not arch.is_changing_mood and
            arch.loving_compliment and 
            arch.mood == archlib.MOOD.BOOTING_UP or
            arch.mood == archlib.MOOD.EATING or
            arch.mood == archlib.MOOD.WAKING_UP):
            return
        else:
            arch.is_changing_mood = True

        arch.button_clicked += 1

        if arch.button_clicked == 1 and arch.mood == archlib.MOOD.DEFAULT:
            arch.mood = archlib.MOOD.SUS

        if arch.button_clicked == 2 and arch.mood == archlib.MOOD.SUS:
            arch.mood = archlib.MOOD.LOVING

        if arch.mood == archlib.MOOD.LOVING:
            arch.loving_compliment = True
        print("Button pressed times:", arch.button_clicked)

button = Pin(19, Pin.IN, Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed)

def happy_birthday():
    t = time.localtime()
    # 22.04
    month = t[1]
    day   = t[2]

    if month == 4 and day == 22:
        print("Happy birthday, Ecenur!")

def booting_up_mood():
    fb.fill(0)
    flush_buffer()
    boot()
    booting_eyes()
    greeting()
    arch.mood = archlib.MOOD.DEFAULT
    time.sleep(1)

def render_mood():
    if arch.mood == archlib.MOOD.BOOTING_UP:
        booting_up_mood()
    if arch.mood == archlib.MOOD.DEFAULT:
        default_mood()
    elif arch.mood == archlib.MOOD.HUNGRY:
        hungry_mood()
    elif arch.mood == archlib.MOOD.SLEEPING:
        sleeping_mood()
    elif arch.mood == archlib.MOOD.WAKING_UP:
        waking_up_mood()
    elif arch.mood == archlib.MOOD.ANGRY:
        angry_mood()
    elif arch.mood == archlib.MOOD.TIRED:
        tired_mood()
    elif arch.mood == archlib.MOOD.SAD:
        sad_mood()
    elif arch.mood == archlib.MOOD.LOVING:
        loving_mood()
    elif arch.mood == archlib.MOOD.SUS:
        sus_mood()
    elif arch.mood == archlib.MOOD.EATING:
        eating_mood()

def main():
    while True:
        arch.mood = archlib.MOOD.DEFAULT
        render_mood()
    # TODO: Implement check of happy_birthday on each mode

main()
