import CamerPlaying as cam
from time import sleep
from gpiozero import LED

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pi
led = LED(3)


runningSample = False
buttonPressed = False

def CheckButtonPress():
    global buttonPressed
    global runningSample
    if buttonPressed and GPIO.input(2) == GPIO.HIGH and runningSample == False:
        runningSample = True
        buttonPressed = False
        led.on()
        cam.RecordWholeSample(0)
        runningSample = False
    elif GPIO.input(2) == GPIO.LOW:
        buttonPressed = True
    

while True:
    led.off()
    CheckButtonPress()
    sleep(0.05)

