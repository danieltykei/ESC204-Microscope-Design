import board
import digitalio
import time
# Configure the internal GPIO connected to the LED as a digital output
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
print('Hello! My LED is blinking now.')
while True:
    led.value = True  # Turn on the LED
    time.sleep(0.5)  # wait 0.5 seconds
    led.value = False  # Turn off the LED
    time.sleep(0.5)  # wait 0.5 seconds
