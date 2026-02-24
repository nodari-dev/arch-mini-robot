from lib import constants

class Mood:
    DEFAULT = 0
    HUNGRY = 1
    SLEEPING = 2
    ANGRY = 3
    TIRED = 4
    SAD = 5
    LOVING = 6
    SUS = 7
    EATING = 8


class Eye:
  w = constants.DEFAULT_EYE_W
  h = constants.DEFAULT_EYE_H
  x = 0
  y = constants.DEFAULT_EYE_Y

class Mouth:
  r = constants.DEFAULT_MOUTH_R
  x = constants.DEFAULT_MOUTH_X
  y = constants.DEFAULT_MOUTH_Y

class Drool:
  w = constants.DEFAULT_DROOL_W
  h = constants.DEFAULT_DROOL_H
  x = constants.DEFAULT_DROOL_X
  y = constants.DEFAULT_DROOL_Y

class Archi:
    # action_button = button
    left_eye = Eye()
    right_eye = Eye()
    mouth = Mouth()
    drool = Drool()
    last_button_state = 1
    mood = Mood.DEFAULT
    last_look_action: str | None = None
    hunger = 0
    tiredness = 0
    button_clicked = 0
    anger = 0
    annoyanse = 0
