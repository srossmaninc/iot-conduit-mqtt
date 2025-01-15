from sense_hat import SenseHat
import subprocess, time
import sense_shared as sym

# <---SENSE HAT & COLORS--->
s = SenseHat()
s.low_light = True

"""
currColor lets us use the same animation variable regardless of the status
 with us being able to change the color inside a conditional
"""
currColor = (0, 0, 0)

# <---MAIN LOGIC--->
print("running...")
count = 0
while(True):
    stages = sym.broker_stages(currColor)
    if (count % 15 == 0):
        """
        every 30 seconds (count * 1.5) (count starts at 0 so technically first gap is 16 seconds?
        checking if mosquitto is working
        """
        proc = subprocess.Popen('sudo systemctl status mosquitto', shell=True, stdout=subprocess.PIPE, )
        output, errors = proc.communicate()
        output = output.decode("utf-8")
    
    if "active (running)" in output:
        currColor = (255, 255, 0)
    else:
        currColor = (255, 0, 0)
        
    s.set_pixels(stages[count % len(stages)])
    time.sleep(1.5) # sleep for 1.5 seconds
    count += 1