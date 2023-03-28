from flask import Flask, render_template_string, request
import RPi.GPIO as GPIO
from time import sleep
from RpiMotorLib import RpiMotorLib
import math

GPIO_pins_hori = (14, 15, 18)
GPIO_pins_vert = (23, 24, 25)
Hdirection = 20
Hstep = 21
Vdirection = 12
Vstep = 16


# following are variable to determine step size
gearRadius = 5

hSteps = 5 # number of steps before reaching the end
hLength = 10 #cm
hstepSize = hLength / hSteps
hAngle = hstepSize / gearRadius
hsteps = hAngle * 100 / math.pi


vSteps = 5 # number of steps before reaching the end
vLength =10 #cm
vstepSize = vLength / vSteps
vAngle = vstepSize / gearRadius
vsteps = vAngle * 100 / math.pi

verticalMotor = RpiMotorLib.A4988Nema(Vdirection, Vstep, GPIO_pins_vert, "A4988")
horizontalMotor = RpiMotorLib.A4988Nema(Hdirection, Hstep, GPIO_pins_hori, "A4988")

#horizontalMotor.motor_go(True, "Full" , 600,0.01, False, .05)
	
def MoveMotor(rotation, motor):
	# (rotation) 1 = clockwise
	# (rotation) 0 = counter clockwise
	# (motor) = "h" or "v"
	if motor == "h":
		if rotation:
			horizontalMotor.motor_go(True, "Full" , int(hsteps), 0.01, False, .05)
		else:
			horizontalMotor.motor_go(False, "Full" , int(hsteps), 0.01, False, .05)
	elif motor == "v":
		if rotation:
			verticalMotor.motor_go(True, "Full" , int(vsteps), 0.01, False, .05)
		else:
			verticalMotor.motor_go(False, "Full" , int(vsteps), 0.01, False, .05)
	else:
		print("Youssef! please give me an h or a v")
	

for i in range(4):
    MoveMotor(0, "v")
    MoveMotor(0, "v")
    MoveMotor(0, "v")
    MoveMotor(0, "v")
    MoveMotor(0, "v")
    MoveMotor(0, "v")
    MoveMotor(0, "v")
    MoveMotor(0, "v")
    MoveMotor(0, "v")
    MoveMotor(0, "v")
    MoveMotor(1, "v")
    MoveMotor(1, "v")
    MoveMotor(1, "v")
    MoveMotor(1, "v")
    MoveMotor(1, "v")
    MoveMotor(1, "v")
    MoveMotor(1, "v")
    MoveMotor(1, "v")
    MoveMotor(1, "v")
    MoveMotor(1, "v")

    MoveMotor(1, "h")
    MoveMotor(1, "h")
    MoveMotor(1, "h")
    MoveMotor(1, "h")
    MoveMotor(1, "h")
    MoveMotor(1, "h")
    MoveMotor(1, "h")
    MoveMotor(1, "h")
    MoveMotor(1, "h")
    MoveMotor(1, "h")
    MoveMotor(1, "h")
    MoveMotor(0, "h")
    MoveMotor(0, "h")
    MoveMotor(0, "h")
    MoveMotor(0, "h")
    MoveMotor(0, "h")
    MoveMotor(0, "h")
    MoveMotor(0, "h")
    MoveMotor(0, "h")
    MoveMotor(0, "h")
    MoveMotor(0, "h")
    MoveMotor(0, "h")
