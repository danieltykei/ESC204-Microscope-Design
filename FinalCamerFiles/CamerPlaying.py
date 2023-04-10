from picamera import PiCamera
from time import sleep
import numpy as np
from PIL import Image, ImageFilter
import MotorControlPlay as motor
import os

#The Camera module is gonna move the slide in the 1 direction 

picNumber = 0
focalNumber = 0
prevFocus = 100
vertSteps = 0


camera = PiCamera()

def TakePicture(img_path):
    camera.start_preview()
    sleep(0.1)
    camera.capture(img_path)
    camera.stop_preview()
    img = Image.open(img_path)
    #rint(img.format, img.size, img.mode)
    imgdata = list(img.getdata()) # Returns a list of pixels (represented as RGB tupples)
    #print(len(imgdata))
    return img


def F(image):
    imgdata = list(image.getdata())
    I    = lambda RGB : sum(RGB) / 3
    mu   = sum(map(I, imgdata))/np.prod(image.size)
    W, H = image.size
    return 1 / (W * H * mu) * sum(((i - mu)**2 for i in map(I, imgdata)))


def RecordSampleFocus(prevFocus, img_path, focalNumber, picNumber):
        print(img_path)
        img = TakePicture(img_path)
        currentFocus = F(img)
        print("current focus is", currentFocus)
        print("prev focus was", prevFocus)
        if currentFocus < prevFocus and focalNumber == motor.vSteps:
            print("almost fell out") #catch for making sure it doesnt fall out
            for i in range(0, focalNumber):
                motor.MoveMotor(1,"v")
                print("reset the motor")
        elif currentFocus < prevFocus:
            if prevFocus != 100:
                removedPath = r'./images/Sample' + str(picNumber) +'focus' + str(focalNumber - 1)+ '.png'
                os.remove(removedPath)
            focalNumber += 1
            prevFocus = currentFocus
            motor.MoveMotor(0, "v")
            img_path = r'./images/Sample' + str(picNumber) +'focus' + str(focalNumber)+ '.png'
            print(focalNumber)
            RecordSampleFocus(prevFocus, img_path, focalNumber, picNumber)
        else: 
            os.remove(img_path)
            for i in range(0, focalNumber):
                motor.MoveMotor(1,"v")
                print("reset the motor")


def RecordWholeSample(step):
    motor.Reset()
    picNumber = 0
    while step <= motor.hSteps:
        focalNumber = 0
        img_path = r'./images/Sample' + str(picNumber) +'focus' + str(focalNumber)+ '.png'
        RecordSampleFocus(100, img_path, 0, picNumber)
        picNumber += 1
        if step != motor.hSteps:
            motor.MoveMotor(1, "h")
        step += 1
        print("reset step size")
    motor.Reset()
    
    
#RecordWholeSample(0)
    



