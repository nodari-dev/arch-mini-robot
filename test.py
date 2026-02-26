import time

def mood_expired(mood_time):
    # now = time.ticks_ms()
    # return time.ticks_diff(now, mood_time) >= 30000
    now = time.time()
    return (now - mood_time) >= 5

# activity_started = time.ticks_ms()
activity_started = time.time()
print("Started")
while not mood_expired(activity_started):
    print("Working")
    time.sleep(0.2)
print("end")

