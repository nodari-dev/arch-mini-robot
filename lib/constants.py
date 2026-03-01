import st7789py as st7789

DISPLAY_W = 240
DISPLAY_H = 240

BLACK = st7789.color565(0, 0, 0)
WHITE = st7789.color565(255, 255, 255)
RED = st7789.color565(255, 0, 0)
GREEN = st7789.color565(251,104,105)

FONT_WIDTH = 8
FONT_HEIGHT = 16

# EYES
DEFAULT_EYE_W = 60
DEFAULT_EYE_H = 70

DEFAULT_LEFT_EYE_X = 50
DEFAULT_RIGHT_EYE_X = 140

DEFAULT_EYE_Y = 120 - DEFAULT_EYE_H//2
DEFAULT_LOVING_Y = 120 - DEFAULT_EYE_H//2 + 20

# LOOK
LOOK_MOVEMENT_RANGE = 10
LOOK_MOVEMENT_STEP = 2

# MOUTH
DEFAULT_MOUTH_R = 15
DEFAULT_MOUTH_X = 120
DEFAULT_MOUTH_Y = 170

# DROOL
DEFAULT_DROOL_W = 6
DEFAULT_DROOL_H = 30
DEFAULT_DROOL_X = 125
DEFAULT_DROOL_Y = 175

COMPLIMENTS = [
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
