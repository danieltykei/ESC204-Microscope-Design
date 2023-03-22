import time
import board

from analogio import AnalogIn


pot = AnalogIn(board.D14)
print("Started")


'''while True:
    reading = pot.analog_Read(pot)
    time.sleep(300)
    print(reading)


'''
