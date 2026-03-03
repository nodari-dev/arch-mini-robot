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
    REACTION = 7
    EATING = 8
    WAKING_UP = 9
    BOOTING_UP = 10
    BLINK_TEXT = 12

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
    is_changing_mood: bool = False
    mood = MOOD.BOOTING_UP
    loving_compliment: bool = False
    last_look_action: str | None = None
    last_reaction: function | None = None
    # button
    last_button_state = 1
    button_clicked = 0
    clicks_to_love = 2
    # physical
    hunger = 0
    tiredness = 0
    anger = 0
    annoyanse = 0
    happiness = 45

    def should_switch_mod(self, mod):
        return self.mood != mod

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

    def sleeping_cycle_completed(self):
        self.change_tiredness(5, increase=False)


    def will_sleep_more(self):
        if self.tiredness > 0:
            self.mood = MOOD.SLEEPING
            return 

    def decide_on_mood(self):
        previous_mood = self.mood
        if self.tiredness == 100:
            print("Im sleeping")
            self.mood = MOOD.SLEEPING
            return 

        if self.tiredness > 35 and previous_mood == MOOD.WAKING_UP:
            print("Im angry after waking up")
            self.mood = MOOD.ANGRY
            return 
        if self.tiredness >= 75:
            print("Im tired")
            self.mood = MOOD.TIRED
            return 
        if self.hunger == 100:
            print("Im hugry")
            self.mood = MOOD.HUNGRY
            return
        else:
            print("Im default")
            self.mood = MOOD.DEFAULT
        # if self.tiredness > 80:
        #     print("tiredness")
        # if self.anger > 50:
        #     print("angry")

    def time_passed(self, mood_time, ms_passed = 3000):
        now = time.ticks_ms()
        return time.ticks_diff(now, mood_time) >= ms_passed
