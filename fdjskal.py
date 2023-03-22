import time
import board
import analogio
from analogio import AnalogIn
import pwmio
import digitalio
from digitalio import DigitalInOut

### CONSTANTS/PARAMETERS
INT_MODE = 0
VOLT_MODE = 1
mode = VOLT_MODE

max_int = 65535
ADC_HIGH = 65535


### PIN SETUP
conductance_sensor = AnalogIn(board.A0)
switch = AnalogIn(board.A1)
led = DigitalInOut(board.A2)
led.direction = digitalio.Direction.OUTPUT

# motor pins (could be wrong for now idek)
pwm_arm = pwmio.PWMOut(board.D6, duty_cycle = 0)
dir_arm_1 = DigitalInOut(board.D7)
dir_arm_2 = DigitalInOut(board.D8)
dir_arm_1.direction = digitalio.Direction.OUTPUT
dir_arm_2.direction = digitalio.Direction.OUTPUT

pwm_pump = pwmio.PWMOut(board.D5, duty_cycle = 0)
dir_pump_1 = DigitalInOut(board.D4)
dir_pump_2 = DigitalInOut(board.D3)
dir_pump_1.direction = digitalio.Direction.OUTPUT
dir_pump_2.direction = digitalio.Direction.OUTPUT

### HELPER FUNCTIONS

def conductance():
    return conductance_sensor.value

def switch_value():
    return (switch.value) # basically is it on based on voltage drop?

### END HELPER FUNCTIONS

### need to test all the pins to see if they are working

led.value = False
arm_test = True
pump_test = True

while True:

    led.value = not led.value
    if arm_test:
        dir_arm_1.value, dir_arm_2.value = (True, False)
        pwm_arm.duty_cycle = 20000
        time.sleep(0.5)
        pwm_arm.duty_cycle = 0
        dir_arm_1.value, dir_arm_2.value = (True, False)
        pwm_arm.duty_cycle = 20000
        time.sleep(0.5)
        pwm_arm.duty_cycle = 0

    if pump_test:
        dir_pump_1.value, dir_pump_2.value = (True, False)
        pwm_pump.duty_cycle = 60000
        #time.sleep(25)
        #pwm_pump.duty_cycle = 0# Write your code here :-)
