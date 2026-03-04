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
    message = random.choice(constants.GREETINGS)
    text_renderer.render_two_text_lines_center(tft, text1=message[0], text2=message[1], color=constants.WHITE)
    time.sleep(3)
    text_renderer.clear_two_whole_lines(tft)

def boot():
    text_renderer.render_text_line_center(tft, "Arch mini", constants.WHITE)
    time.sleep(3)
    text_renderer.clear_two_whole_lines(tft)
    text_renderer.render_two_text_lines_center(tft, "Ecenur", "Edition", constants.WHITE)
    time.sleep(3)
    text_renderer.clear_two_whole_lines(tft)
    text_renderer.clear_whole_line(tft)
    text_renderer.render_two_text_lines_center(tft, "Made with love", "By N", constants.WHITE)
    time.sleep(4)
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

    time.sleep(3)
    text_renderer.clear_whole_line(tft)
    time.sleep(3)

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

    start_time = time.ticks_ms()
    while arch.mood == archlib.MOOD.DEFAULT:
        arch.decide_on_mood()
        if arch.should_switch_mod(archlib.MOOD.DEFAULT):
            break
        if arch.time_passed(start_time, constants.DEFAULT_CYCLE_TIME_MS):
            start_time = time.ticks_ms()
            arch.default_cycle_completed()

        levitate_reps = random.randrange(5, 10)
        for rep in range(levitate_reps):
            arch.decide_on_mood()
            if arch.should_switch_mod(archlib.MOOD.DEFAULT):
                break
            if arch.time_passed(start_time, constants.DEFAULT_CYCLE_TIME_MS):
                start_time = time.ticks_ms()
                arch.default_cycle_completed()
            levitate_default_single()
            rep += 1

        arch.debug_stats()

        look_around_reps = random.randrange(1, 2)
        for rep in range(look_around_reps):
            name, (dx, dy) = random.choice(list(DIRECTIONS.items()))
            arch.decide_on_mood()
            if arch.should_switch_mod(archlib.MOOD.DEFAULT):
                break
            if arch.time_passed(start_time, constants.DEFAULT_CYCLE_TIME_MS):
                start_time = time.ticks_ms()
                arch.default_cycle_completed()
            if name == arch.last_look_action:
                time.sleep(0.5)
                continue
            arch.last_look_action = name
            look_to(dx, dy)
            time.sleep(1)
            look_back_to_center()
            rep += 1

        time.sleep(1)
    render_mood()

def render_hungry_mouth(r=0, drool_height = arch.drool.h):
    # Draw over drool
    fb.fill_rect(0, arch.mouth.y, constants.DISPLAY_W, 60, constants.BLACK)

    # Mouth
    if r == 0:
        r = arch.mouth.r
    graphics.fill_circle(fb, arch.mouth.x, arch.mouth.y, r, constants.WHITE)

    # Drool
    arch.drool.h = drool_height
    fb.fill_rect(arch.drool.x, arch.drool.y, arch.drool.w, arch.drool.h, constants.WHITE)

def render_default_mouth(y=arch.mouth.y, r=arch.mouth.r):
    arch.mouth.r = r
    graphics.fill_circle(fb, arch.mouth.x, y, arch.mouth.r, constants.WHITE)

def blink_with_mouth():
    for h in range(constants.DEFAULT_EYE_H, 5, -16):
        render_eyes(height1=h, height2=h)
        render_hungry_mouth(drool_height=arch.drool.h)
        flush_buffer()
        time.sleep(0.0001)
    for h in range(5, constants.DEFAULT_EYE_H, 16):
        render_eyes(height1=h, height2=h)
        render_hungry_mouth(drool_height=arch.drool.h)
        flush_buffer()
        time.sleep(0.0001)
    time.sleep(0.05)

def hungry_mood():
    render_eyes()
    render_hungry_mouth(r=constants.DEFAULT_MOUTH_R)
    flush_buffer()

    # FINISH ME

    # work around
    # as rpi pico does not have internal clock
    # to make a deep sleep at night, we will check if hunger is 100 for 15 minutes
    # then go to deep sleep

    # if more then 5 minutes > randomly choose angry or sad mood
    # after eating > one 1 in 10 chanse -> fall asleep
    
    start_time = time.ticks_ms()
    while arch.mood == archlib.MOOD.HUNGRY:
        # longer drool
        if random.randrange(1, 3) == 1:
            for h in range(arch.drool.h, arch.drool.h+15, LEVITATION_STEP):
                if arch.should_switch_mod(archlib.MOOD.HUNGRY):
                    break
                # 5 MINUTES PASSED
                if arch.time_passed(start_time, constants.DEFAULT_CYCLE_TIME_MS):
                    start_time = time.ticks_ms()
                    # trigger angry face for 20 seconds
                    # if pressed - feed 
                    # if not - come back hungry mood
                    # arch.default_cycle_completed()
                render_hungry_mouth(drool_height=h)
                flush_buffer()
                time.sleep(0.1)

            time.sleep(0.5)
            # small drip of saliva
            drip_pos = arch.drool.y+arch.drool.h
            fb.fill_rect(arch.drool.x, drip_pos, arch.drool.w, 8, constants.WHITE)
            flush_buffer()

            while drip_pos < constants.DISPLAY_H:
                if arch.should_switch_mod(archlib.MOOD.HUNGRY):
                    break
                fb.fill_rect(arch.drool.x, drip_pos, arch.drool.w, 8, constants.BLACK)
                fb.fill_rect(arch.drool.x, drip_pos+1, arch.drool.w, 8, constants.WHITE)
                flush_buffer()
                drip_pos += 1
                time.sleep(0.01)

            # shorter drool
            for h in range(arch.drool.h, arch.drool.h-15, -LEVITATION_STEP):
                if arch.should_switch_mod(archlib.MOOD.HUNGRY):
                    break
                render_hungry_mouth(drool_height=h)
                flush_buffer()
                time.sleep(0.01)

        if random.randrange(1, 3) == 1:
            if arch.should_switch_mod(archlib.MOOD.HUNGRY):
                break
            blink_with_mouth()
        else:
            time.sleep(1)
    render_mood()

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
    mood_start_time = time.ticks_ms()
    while arch.mood == archlib.MOOD.ANGRY and not arch.time_passed(mood_time=mood_start_time, ms_passed=5000):
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

def sus_emote():
    for h in range(arch.left_eye.h, 30, -5):
        render_eyes(height1=h, height2=h)
        flush_buffer()
        time.sleep(0.0001)

    time.sleep(2.5)

    for h in range(arch.left_eye.h, 65, 5):
        if arch.should_switch_mod(archlib.MOOD.REACTION):
            break
        render_eyes(height1=h, height2=h)
        flush_buffer()
        time.sleep(0.0001)

def blink_one_eye():
    for h in range(arch.left_eye.h, 5, -10):
        render_eyes(height1=arch.left_eye.h, height2=h)
        flush_buffer()
        time.sleep(0.0001)

    time.sleep(0.1)

    for h in range(5, constants.DEFAULT_EYE_H, 10):
        render_eyes(height1=arch.left_eye.h, height2=h)
        flush_buffer()
        time.sleep(0.0001)

def whoa():
    for h in range(arch.left_eye.h, 30, -10):
        render_eyes(height1=arch.left_eye.h, height2=h)
        flush_buffer()
        time.sleep(0.0001)
    for r in range(5, 15, 1):
        render_eyes(height1=arch.left_eye.h, height2=arch.right_eye.h)
        render_default_mouth(r=r)
        flush_buffer()
        time.sleep(0.0001)
    time.sleep(1)
    for r in range(15, 0, -1):
        render_eyes(height1=arch.left_eye.h, height2=arch.right_eye.h)
        render_default_mouth(r=r)
        flush_buffer()
        time.sleep(0.0001)
    time.sleep(1)
    
def smile():
    for h in range(arch.left_eye.h, 50, -10):
        render_eyes(height1=h, height2=h)
        flush_buffer()
        time.sleep(0.0001)
    for w in range(0, 70, 10):
        fb.fill(0)
        render_eyes(height1=arch.left_eye.h, height2=arch.right_eye.h)
        graphics.draw_cute_smile(
            fb,
            cx=120,
            cy=175,
            width=w,
            depth=-15,
            thickness=10,
            color=constants.WHITE)
        flush_buffer()
        time.sleep(0.0001)

    time.sleep(3)
    
    for h in range(50, constants.DEFAULT_EYE_H, 10):
        render_eyes(height1=h, height2=h)
        flush_buffer()
        time.sleep(0.0001)

emotes = [sus_emote, blink_one_eye, whoa, smile]
def reaction_mood():
    animation = random.choice(emotes)
    while animation == arch.last_reaction:
        animation = random.choice(emotes)
    arch.last_reaction = animation
    animation()

    arch.reaction_was_called = False
    arch.decide_on_mood()
    render_mood()

def sleeping_mood():
    # if woken up during the sleep and tiredness >= 50
    # WAKE UP
    # SHOW ANGER
    # FALL ASLEEP AGAIN

    for h in range(arch.left_eye.h, 5, -1):
        render_eyes(height1=h, height2=h)
        flush_buffer()
        time.sleep(0.0001)

    start_time = time.ticks_ms()
    while arch.mood == archlib.MOOD.SLEEPING and arch.tiredness != 0:
        for r in range(arch.mouth.r, 23, 1):
            if arch.should_switch_mod(archlib.MOOD.SLEEPING):
                break
            if arch.time_passed(start_time, constants.DEFAULT_CYCLE_TIME_MS):
                start_time = time.ticks_ms()
                arch.sleeping_cycle_completed()
            render_eyes(height1=arch.left_eye.h, height2=arch.right_eye.h)
            render_default_mouth(r=r)
            flush_buffer()
            time.sleep(0.01)

        time.sleep(0.5)
        print("tiredness:", arch.tiredness)

        for r in range(arch.mouth.r, 0, -1):
            if arch.should_switch_mod(archlib.MOOD.SLEEPING):
                break
            if arch.should_switch_mod(archlib.MOOD.SLEEPING):
                start_time = time.ticks_ms()
                arch.sleeping_cycle_completed()
            render_eyes(height1=arch.left_eye.h, height2=arch.right_eye.h)
            render_default_mouth(r=r)
            flush_buffer()
            time.sleep(0.01)
        print("tiredness:", arch.tiredness)
        time.sleep(2.5)
    arch.mood = archlib.MOOD.WAKING_UP
    render_mood()

def tired_mood():
    # SLOWLY squise eys
    # FAST open it
    # randomly SLOW look around
    # no levitaion

    render_eyes()
    flush_buffer()

    start_time = time.ticks_ms()
    while arch.mood == archlib.MOOD.TIRED:
        arch.decide_on_mood()
        if arch.should_switch_mod(archlib.MOOD.TIRED):
            break

        arch.debug_stats() 

        if arch.time_passed(start_time, constants.DEFAULT_CYCLE_TIME_MS):
            start_time = time.ticks_ms()
            arch.default_cycle_completed()

        if random.randrange(1, 5) == 1:
            for h in range(arch.left_eye.h, 5, -1):
                arch.decide_on_mood()
                if arch.should_switch_mod(archlib.MOOD.TIRED):
                    break

                if arch.time_passed(start_time, constants.DEFAULT_CYCLE_TIME_MS):
                    start_time = time.ticks_ms()
                    arch.default_cycle_completed()
                render_eyes(height1=h, height2=h)
                flush_buffer()
                time.sleep(0.0001)

            time.sleep(1)

            for r in range(arch.mouth.r, 23, 1):
                arch.decide_on_mood()
                if arch.should_switch_mod(archlib.MOOD.TIRED):
                    break

                if arch.time_passed(start_time, constants.DEFAULT_CYCLE_TIME_MS):
                    start_time = time.ticks_ms()
                    arch.default_cycle_completed()
                render_eyes(height1=arch.left_eye.h, height2=arch.right_eye.h)
                render_default_mouth(r=r)
                flush_buffer()
                time.sleep(0.01)

            time.sleep(1)

            for r in range(arch.mouth.r, 0, -1):
                arch.decide_on_mood()
                if arch.should_switch_mod(archlib.MOOD.TIRED):
                    break

                if arch.time_passed(start_time, constants.DEFAULT_CYCLE_TIME_MS):
                    start_time = time.ticks_ms()
                    arch.default_cycle_completed()
                render_eyes(height1=arch.left_eye.h, height2=arch.right_eye.h)
                render_default_mouth(r=r)
                flush_buffer()
                time.sleep(0.01)

            time.sleep(1)
                
            for h in range(arch.left_eye.h, constants.DEFAULT_EYE_H, 5):
                arch.decide_on_mood()
                if arch.should_switch_mod(archlib.MOOD.TIRED):
                    break

                if arch.time_passed(start_time, constants.DEFAULT_CYCLE_TIME_MS):
                    start_time = time.ticks_ms()
                    arch.default_cycle_completed()
                render_eyes(height1=h, height2=h)
                flush_buffer()
                time.sleep(0.0001)
            time.sleep(1)

        if random.randrange(1, 3) == 1:
            for h in range(arch.left_eye.h, 5, -1):
                arch.decide_on_mood()
                if arch.should_switch_mod(archlib.MOOD.TIRED):
                    break

                if arch.time_passed(start_time, constants.DEFAULT_CYCLE_TIME_MS):
                    start_time = time.ticks_ms()
                    arch.default_cycle_completed()
                render_eyes(height1=h, height2=h)
                flush_buffer()
                time.sleep(0.0001)

            time.sleep(3)

            for h in range(arch.left_eye.h, constants.DEFAULT_EYE_H, 5):
                arch.decide_on_mood()
                if arch.should_switch_mod(archlib.MOOD.TIRED):
                    break

                if arch.time_passed(start_time, constants.DEFAULT_CYCLE_TIME_MS):
                    start_time = time.ticks_ms()
                    arch.default_cycle_completed()
                render_eyes(height1=h, height2=h)
                flush_buffer()
                time.sleep(0.0001)
            time.sleep(1)

        levitation_steps = random.randrange(1, 6)
        # levitate
        for step in range(levitation_steps):
            for y in range(arch.left_eye.y, arch.left_eye.y+15, LEVITATION_STEP):
                arch.decide_on_mood()
                if arch.should_switch_mod(archlib.MOOD.TIRED):
                    break

                if arch.time_passed(start_time, constants.DEFAULT_CYCLE_TIME_MS):
                    start_time = time.ticks_ms()
                    arch.default_cycle_completed()
                render_eyes(y1=y, y2=y)
                flush_buffer()
                time.sleep(0.01)

            for y in range(arch.left_eye.y, arch.left_eye.y-15, -LEVITATION_STEP):
                arch.decide_on_mood()
                if arch.should_switch_mod(archlib.MOOD.TIRED):
                    break

                if arch.time_passed(start_time, constants.DEFAULT_CYCLE_TIME_MS):
                    start_time = time.ticks_ms()
                    arch.default_cycle_completed()
                render_eyes(y1=y, y2=y)
                flush_buffer()
                time.sleep(0.01)

            for y in range(arch.left_eye.y, arch.left_eye.y+15, LEVITATION_STEP):
                arch.decide_on_mood()
                if arch.should_switch_mod(archlib.MOOD.TIRED):
                    break

                if arch.time_passed(start_time, constants.DEFAULT_CYCLE_TIME_MS):
                    start_time = time.ticks_ms()
                    arch.default_cycle_completed()
                render_eyes(y1=y, y2=y)
                flush_buffer()
                time.sleep(0.01)

            for y in range(arch.left_eye.y, arch.left_eye.y-15, -LEVITATION_STEP):
                arch.decide_on_mood()
                if arch.should_switch_mod(archlib.MOOD.TIRED):
                    break

                if arch.time_passed(start_time, constants.DEFAULT_CYCLE_TIME_MS):
                    start_time = time.ticks_ms()
                    arch.default_cycle_completed()
                render_eyes(y1=y, y2=y)
                flush_buffer()
                time.sleep(0.01)

            step += 1
        time.sleep(1)

    render_mood()

def pick_compliment():
    fb.fill(0)
    flush_buffer()
    compliment_index = arch.last_compliment_index
    while compliment_index == arch.last_compliment_index:
        compliment_index = random.randint(0, len(constants.COMPLIMENTS) - 1)
    arch.last_compliment_index = compliment_index

    lines = constants.COMPLIMENTS[compliment_index]
    text_renderer.render_three_text_lines_center(tft, lines[0], lines[1], lines[2], constants.WHITE)

def should_show_compliment():
    if (arch.loving_compliment):
        pick_compliment()
        time.sleep(2)
        arch.loving_compliment = False

def loving_mood():
    mood_start_time = time.ticks_ms()
    while arch.mood == archlib.MOOD.LOVING and not arch.time_passed(mood_time=mood_start_time, ms_passed=constants.THIRTY_SECONDS_MS):
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
    for h in range(arch.left_eye.h, 5, -1):
        render_eyes(height1=h, height2=h)
        flush_buffer()
        time.sleep(0.0001)

    mood_start_time = time.ticks_ms()
    while arch.mood == archlib.MOOD.EATING and not arch.time_passed(mood_start_time):
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

        for h in range(arch.left_eye.h, constants.DEFAULT_EYE_H, 2):
            fb.fill(0)
            render_eyes(height1=h, height2=h)
            flush_buffer()
            time.sleep(0.002)

    arch.hunger = 0

def waking_up_mood():
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

last_press_time = 0
def button_pressed(pin):
    global last_press_time

    current_time = time.ticks_ms()

    if time.ticks_diff(current_time, last_press_time) > 200:
        last_press_time = current_time
        # IGNORE IF SPECIFIC MODE IS ENABLED
        if (arch.is_changing_mood or
            arch.loving_compliment or
            arch.mood == archlib.MOOD.BOOTING_UP or
            arch.mood == archlib.MOOD.EATING or
            arch.mood == archlib.MOOD.WAKING_UP):
            return

        if arch.mood == archlib.MOOD.HUNGRY:
            arch.prev_mood = arch.mood
            arch.mood = archlib.MOOD.EATING
            return

        if arch.mood == archlib.MOOD.SLEEPING:
            arch.prev_mood = arch.mood
            arch.mood = archlib.MOOD.WAKING_UP
            return
        
        if arch.mood == archlib.MOOD.LOVING:
            arch.loving_compliment = True
            return

        arch.button_clicked += 1
        if (arch.button_clicked == arch.clicks_to_love):
            arch.prev_mood = arch.mood
            arch.mood = archlib.MOOD.LOVING
            arch.clicks_to_love = random.randrange(2, 7)
            arch.change_tiredness(5)
            arch.change_hunger(5)
            arch.button_clicked = 0
            arch.loving_compliment = True
            return
        else:
            arch.change_tiredness(5)
            arch.change_hunger(5)
            arch.mood = archlib.MOOD.REACTION
            arch.reaction_was_called = True
            return

button = Pin(19, Pin.IN, Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed)


def booting_up_wake_up():
    fb.fill(0)
    flush_buffer()

    # eyes on the bottom
    for y in range(240, 195, -4):
        render_eyes(y1=y, y2=y)
        flush_buffer()
        time.sleep(0.0001)
    time.sleep(1)

    for y in range(195, 245, 6):
        render_eyes(y1=y, y2=y)
        flush_buffer()
        time.sleep(0.0001)
    time.sleep(2)

    # eyes on the top
    for y in range(-constants.DEFAULT_EYE_Y -10, -25, 4):
        render_eyes(y1=y, y2=y)
        flush_buffer()
        time.sleep(0.0001)

    time.sleep(1)

    for y in range(-25, -constants.DEFAULT_EYE_Y - 10, -6):
        render_eyes(y1=y, y2=y)
        flush_buffer()
        time.sleep(0.0001)
    time.sleep(1)

    for h in range(0, constants.DEFAULT_EYE_H, 4):
        render_eyes(height1=h, height2=h)
        flush_buffer()
        time.sleep(0.0001)
    time.sleep(1)

    blink_default_eyes()
    blink_default_eyes()
    time.sleep(1)

    for h in range(constants.DEFAULT_EYE_H, constants.DEFAULT_EYE_H//2, -4):
        render_eyes(height1=h, height2=h)
        flush_buffer()
        time.sleep(0.0001)
    time.sleep(3)

def booting_up_mood():
    fb.fill(0)
    flush_buffer()
    boot()
    booting_up_wake_up()
    greeting()
    time.sleep(1)

def render_mood():
    if arch.mood == archlib.MOOD.BOOTING_UP:
        booting_up_mood()
    elif arch.mood == archlib.MOOD.DEFAULT:
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
    elif arch.mood == archlib.MOOD.REACTION:
        reaction_mood()
    elif arch.mood == archlib.MOOD.EATING:
        eating_mood()

def main():
    init_flag = True
    test_flag = True
    while True:
        if test_flag:
            arch.hunger = 100
            test_flag = False
        # arch.decide_on_mood(init=init_flag)
        arch.decide_on_mood()
        init_flag = False
        render_mood()

main()
