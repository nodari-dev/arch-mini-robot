import random
import constants
import time

class MOOD:
    DEFAULT = 0
    HUNGRY = 1
    SLEEPING = 2
    ANGRY = 3
    TIRED = 4
    SAD = 5
    LOVING = 6
    SUS = 7
    EATING = 8
    WAKING_UP = 9

class MOOD_FACTOR:
    HUNGER = 0
    TIREDNRESS = 1
    ANGER = 2
    HAPPINESS = 3
    LOVING = 4

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
    left_eye = Eye()
    right_eye = Eye()
    mouth = Mouth()
    drool = Drool()
    mood = MOOD.DEFAULT
    loving_compliment: bool = False
    last_look_action: str | None = None
    # button
    last_button_state = 1
    button_clicked = 0
    # physical
    hunger = 0
    tiredness = 0
    anger = 0
    annoyanse = 0
    happiness = 45

    def should_switch_mod(self, mod):
        return self.mood != mod

    def mood_system(self):
        # 1. happy
        # 2. sad - based on happy
        # 3. angry
        # 4. loving
        # 5. sus
        # 6. sleeping
        # 7. hungry
        # 8. tired
        # 9. default
        
        # combine multiple moods
        # if not hungry anymore and still tired > show next emotion

        
        # SLEEPING 
        #   1. specific time of a day
        #   2. after food
        #   3. can be woken up
        #   4. count down the tiredness
        #   5. if tiredness => 50 then angry face

        if self.hunger > 50:
            print("hugry")
        if self.tiredness > 50:
            print("tiredness")
        if self.anger > 50:
            print("angry")
        if self.annoyanse > 50:
            print("annoyanse")
        if self.happiness > 50:
            print("annoyanse")
        if self.happiness < 25:
            print("sad")

    def min20_passed(self):
        self.hunger += 10
        self.tiredness += 10
        if self.hunger > 60:
            self.happiness -= 5

    def change_tiredness(self, value, increase = True):
        if increase:
            self.tiredness = max(0, min(self.tiredness+value, 100))
        else:
            self.tiredness = max(0, min(self.tiredness-value, 100))

    def change_hunger(self, value, increase = True):
        if increase:
            self.hunger = max(0, min(self.hunger+value, 100))
        else:
            self.hunger = max(0, min(self.hunger-value, 100)) 

    def change_happiness(self, value, increase = True):
        if increase:
            self.happiness = max(0, min(self.happiness+value, 100))
        else:
            self.happiness = max(0, min(self.happiness-value, 100))

    def change_anger(self, value, increase = True):
        if increase:
            self.anger = max(0, min(self.anger+value, 100))
        else:
            self.anger = max(0, min(self.anger-value, 100))

    def change_annoy(self, value, increase = True):
        if increase:
            self.anger = max(0, min(self.anger+value, 100))
        else:
            self.anger = max(0, min(self.anger-value, 100))

    def eating_completed(self):
        self.hunger = 0
        self.happiness += 40
        # can fall asleep after meal
        if random.randint(1, 5) == 1:
            self.tiredness = 100

def time_for_mood_expired(mode_time):
    now = time.ticks_ms()
    return time.ticks_diff(now, mode_time) >= 30000
