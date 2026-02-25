import constants
import graphics
import display
import arch

def render_hearts(display: display.Display):
    display.fb.fill(0)

    graphics.draw_heart(display.fb, 80, 120, 70, constants.WHITE)
    graphics.draw_heart(display.fb, 160, 120, 70, constants.WHITE)

    display.flush_buffer()

def render_default_eyes(
        archi: arch.Arch, 
        screen: display.Display,
        height1=constants.DEFAULT_EYE_H,
        width1=constants.DEFAULT_EYE_W,
        height2=constants.DEFAULT_EYE_H,
        width2=constants.DEFAULT_EYE_W,
        x1=constants.DEFAULT_LEFT_EYE_X, x2=constants.DEFAULT_RIGHT_EYE_X, y1 = 0, y2 = 0,
    ):
    screen.fb.fill(0)

    y1 = 120 - height1//2 if y1 == 0 else y1
    y2 = 120 - height2//2 if y2 == 0 else y2

    # left eye
    archi.left_eye.x = x1
    archi.left_eye.y = y1
    archi.left_eye.w = width1
    archi.left_eye.h = height1
    graphics.draw_eye(screen.fb, x1, y1, width1, height1, 10, constants.WHITE)

    # right eye
    archi.right_eye.x = x2
    archi.right_eye.y = y2
    archi.right_eye.w = width2
    archi.right_eye.h = height2
    graphics.draw_eye(screen.fb, x2, y2, width2, height2, 10, constants.WHITE)

    # tft.blit_buffer(buffer, 0, 0, constants.DISPLAY_W, constants.DISPLAY_H)

def render_sad_eyes(
        archi: arch.Arch, 
        screen: display.Display,
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
    screen.fb.fill(0)

    y1 = 120 - height1//2 if y1 == 0 else y1
    y2 = 120 - height2//2 if y2 == 0 else y2

    # left eye
    archi.left_eye.x = x1
    archi.left_eye.y = y1
    archi.left_eye.w = width1
    archi.left_eye.h = height1
    graphics.fill_polygon(screen.fb, points_left, constants.WHITE)

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
    graphics.fill_polygon(screen.fb, points_right, constants.WHITE)

def render_angry_eyes(
        archi: arch.Arch, 
        screen: display.Display,
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

    screen.fb.fill(0)

    y1 = 120 - height1//2 if y1 == 0 else y1
    y2 = 120 - height2//2 if y2 == 0 else y2
    # left eye
    archi.left_eye.x = x1
    archi.left_eye.y = y1
    archi.left_eye.w = width1
    archi.left_eye.h = height1
    graphics.fill_polygon(screen.fb, points_left, constants.WHITE)

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
    graphics.fill_polygon(screen.fb, points_right, constants.WHITE)

