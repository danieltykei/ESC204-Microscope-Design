import time
import board
import digitalio
from digitalio import DigitalInOut, Direction
from adafruit_motor import stepper

DELAY = 0.01
STEPS = 2000

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

# set up motor command pins as outputs
# Remember: these are the pins for the ARDUINO NANO RP2040 CONNECT not the Pico:
coils = (
    digitalio.DigitalInOut(board.D2),  # IN4
    digitalio.DigitalInOut(board.D3),  # IN3
    digitalio.DigitalInOut(board.D4),  # IN2
    digitalio.DigitalInOut(board.D5),  # IN1
)
for coil in coils:
    coil.direction = digitalio.Direction.OUTPUT

# use the stepper motor library to set up motor output
motor = stepper.StepperMotor(coils[0], coils[1], coils[2], coils[3], microsteps=None)

# run the motor forward
# for step in range(STEPS):

for step in range(STEPS):
    motor.onestep(style=stepper.DOUBLE)
    time.sleep(DELAY)
'''
while True:
    # run the motor backward
    for step in range(STEPS):
        motor.onestep()
        time.sleep(DELAY)

    for step in range(STEPS):
        motor.onestep(direction=stepper.BACKWARD)
        time.sleep(DELAY)
    # run the motor forward with higher torque
    for step in range(STEPS):
        motor.onestep(style=stepper.DOUBLE)
        time.sleep(DELAY)

    # run the motor backward with higher torque
    for step in range(STEPS):
        motor.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        time.sleep(DELAY)

    # run the motor forward and alternate torque levels
    for step in range(STEPS):
        motor.onestep(style=stepper.INTERLEAVE)
        time.sleep(DELAY)

    # run the motor backward and alternate torque levels
    for step in range(STEPS):
        motor.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
        time.sleep(DELAY)
        time.sleep(DELAY)

    # clear coils so no power is sent to motor & shaft can spin freely
    motor.release()
'''

