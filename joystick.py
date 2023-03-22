import time
import board
import digitalio
from adafruit_motor import stepper
from analogio import AnalogIn

DELAY = 0.01

# set up analog input for horizontal and vertical
analog_in_horizontal = AnalogIn(board.A0)

# set up motor command pins as outputs
# Remember: these are the pins for the ARDUINO NANO RP2040 CONNECT not the Pico:
coils_horizontal = (
    digitalio.DigitalInOut(board.D2),  # IN4
    digitalio.DigitalInOut(board.D3),  # IN3
    digitalio.DigitalInOut(board.D4),  # IN2
    digitalio.DigitalInOut(board.D5))  # IN1


for coil in coils_horizontal:
    coil.direction = digitalio.Direction.OUTPUT
    
motor_horizontal = stepper.StepperMotor(coils_horizontal[0], 
                                        coils_horizontal[1], 
                                        coils_horizontal[2], 
                                        coils_horizontal[3], 
                                        microsteps=None)
                                        
def get_voltage(pin):
    return (pin.value * 3.3) / 65536
    
def main():
    while True:
        horizontal_value = get_voltage(analog_in_horizontal)
        print(horizontal_value)
        # turn motor horizontally depending on horizontal input
        if horizontal_value > 3.10:
            print("turn right")
            motor_horizontal.onestep()
        
        elif horizontal_value < 0.50:
            print("turn left")
            motor_horizontal.onestep(direction=stepper.BACKWARD)
        
        time.sleep(DELAY)

if __name__ == "__main__":
    main()
