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


oil_c_min = 0 ## need values for these parameters
oil_c_max = 164 ## I think that ideally theres a max and min conductance that we should check to activate the pump



### PIN SETUP
conductance_sensor = AnalogIn(board.A0)
switch = AnalogIn(board.A1)
emergency_switch = AnalogIn(board.A3)
led = DigitalInOut(board.A2)
led.direction = digitalio.Direction.OUTPUT

# motor pins (could be wrong for now idek)
pwm_arm = pwmio.PWMOut(board.D2, duty_cycle = 0)
dir_arm_1 = DigitalInOut(board.D3)
dir_arm_2 = DigitalInOut(board.D4)
dir_arm_1.direction = digitalio.Direction.OUTPUT
dir_arm_2.direction = digitalio.Direction.OUTPUT

pwm_pump = pwmio.PWMOut(board.D7, duty_cycle = 0)
dir_pump_1 = DigitalInOut(board.D5)
dir_pump_2 = DigitalInOut(board.D6)
dir_pump_1.direction = digitalio.Direction.OUTPUT
dir_pump_2.direction = digitalio.Direction.OUTPUT


### END PIN SETUP

### HELPER FUNCTIONS

def conductance():
    return conductance_sensor.value

def switch_value():
    return (switch.value > 64000) # basically is it on based on voltage drop?

def emergency():
    return (emergency_switch.value > 64000)


### END HELPER FUNCTIONS

### MAIN LOOP

motor_depth = 0
motor_depth_max = 3 # constant need to find
run_pr = True

while True:
    if switch_value() and not run_pr:
        run_pr = True
        led.value = True

    if emergency() and run_pr:
        pwm_pump.duty_cycle = 0
        dir_arm_1, dir_arm_2 = (False, True)
        pwm_arm.duty_cycle = 40000
        time.sleep(motor_depth*1.25)  # need some constant since its harder to pull the arm up than to let it down
        pwm_arm.duty_cycle = 0
        motor_depth = 0
        run_pr = False
        led.value = False

    if run_pr:
        cond = conductance()
        print(cond)

        if cond <= 164:
            if motor_depth > motor_depth_max:
                #reset, all the water has been pumped out
                pwm_pump.duty_cycle = 0
                dir_arm_1, dir_arm_2 = (False, True)
                pwm_arm.duty_cycle = 30000
                time.sleep(motor_depth*1.25)  # need some constant since its harder to pull the arm up than to let it down
                pwm_arm.duty_cycle = 0
                motor_depth = 0
                run_pr = False
                led.value = False

            # case 1: hit oil/air, need to move arm down
            # if the arm doesnt move down, (encoder) we are done, need to reset to top
            else:
                # move arm down
                pwm_pump.duty_cycle = 0
                dir_arm_1, dir_arm_2 = (True, False) # need to check direction
                pwm_arm.duty_cycle = 40000
                time.sleep(1)
                pwm_arm.duty_cycle = 0
                motor_depth += 1


        else:
            # pump out water until we hit oil/air again, which we will becuase of the design of the project
            pwm_pump.duty_cycle = 65535
            dir_pump_1, dir_pump_2 = (True, False)


        # case 2: hit water, need to run the pump until we no longer hit water





### OLD

"""
while True:

    if switch_value() and not run_pr:
        run_pr = True
        led.value = True

    if emergency() and run_pr:
        pwm_pump.duty_cycle = 0
        dir_arm_1, dir_arm_2 = (False, True)
        pwm_arm.duty_cycle = 40000
        time.sleep(motor_depth*1.25)  # need some constant since its harder to pull the arm up than to let it down
        pwm_arm.duty_cycle = 0
        motor_depth = 0
        run_pr = False
        led.value = False

    if run_pr:
        cond = conductance()

        if (cond < oil_c_min): # we have not hit oil yet, lower the arm
            pwm_pump.duty_cycle = 0
            dir_arm_1, dir_arm_2 = (True, False)
            pwm_arm.duty_cycle = 40000
            time.sleep(2)
            pwm_arm.duty_cycle = 0
            motor_depth += 2
        elif (cond >= oil_c_min and cond <= oil_c_max):
            dir_pump_1, dir_pump_2 = (True, False) # pump the oil
            pwm_pump.duty_cycle = 65535
        elif (cond > oil_c_max): # we have hit water, need to reset since the assumption is that we have sucked all the oil
            pwm_pump.duty_cycle = 0
            dir_arm_1, dir_arm_2 = (False, True)
            pwm_arm.duty_cycle = 40000
            time.sleep(motor_depth)
            pwm_arm.duty_cycle = 0
            motor_depth = 0
            led.value = False
            run_pr = False

"""
