from sense_hat import SenseHat
import subprocess, time

s = SenseHat()
s.low_light = True

# currColor lets us use the same animation variable regardless of the status
#   with us being able to change the color inside a conditional
currColor = (0, 0, 0)
O = (0, 0, 0)

def broker_stage_1():
    C = currColor
    bro_stage_1 = [
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, C, C, O, O, O,
    O, O, C, O, O, C, O, O,
    O, O, C, O, O, C, O, O,
    O, O, O, C, C, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    ]
    return bro_stage_1
    
def broker_stage_2():
    C = currColor
    bro_stage_2 = [
    O, O, O, O, O, O, O, O,
    O, O, C, C, C, C, O, O,
    O, C, O, O, O, O, C, O,
    O, C, O, O, O, O, C, O,
    O, C, O, O, O, O, C, O,
    O, C, O, O, O, O, C, O,
    O, O, C, C, C, C, O, O,
    O, O, O, O, O, O, O, O,
    ]
    return bro_stage_2

def broker_stage_3():
    C = currColor
    bro_stage_3 = [
    O, O, C, C, C, C, O, O,
    O, C, O, O, O, O, C, O,
    C, O, O, O, O, O, O, C,
    C, O, O, O, O, O, O, C,
    C, O, O, O, O, O, O, C,
    C, O, O, O, O, O, O, C,
    O, C, O, O, O, O, C, O,
    O, O, C, C, C, C, O, O,
    ]
    return bro_stage_3

stages = [broker_stage_1, broker_stage_2, broker_stage_3]

count = 0

print("running...")

while(True):
    if (count % 15 == 0):
        # every 30 seconds (count * 1.5) (count starts at 0 so technically first gap is 16 seconds?
        # checking if mosquitto is working
        proc = subprocess.Popen('sudo systemctl status mosquitto', shell=True, stdout=subprocess.PIPE, )
        output, errors = proc.communicate()
        output = output.decode("utf-8")
    
    if "active (running)" in output:
        currColor = (255, 255, 0)
    else:
        currColor = (255, 0, 0)
        
    s.set_pixels(stages[count % len(stages)]())
    time.sleep(1.5) # sleep for 1.5 seconds
    count += 1