from picamera import PiCamera
from time import sleep
import numpy as np
from PIL import Image, ImageFilter

img_path = r'./0324_stats/5cm.png'

camera = PiCamera()

camera.start_preview()
sleep(5)
camera.capture(img_path)
camera.stop_preview()


img = Image.open(img_path)
print(img.format, img.size, img.mode)


imgdata = list(img.getdata()) # Returns a list of pixels (represented as RGB tupples)
print(len(imgdata))

def F(image):
    imgdata = list(image.getdata())
    I    = lambda RGB : sum(RGB) / 3
    mu   = sum(map(I, imgdata))/np.prod(image.size)
    W, H = image.size
    return 1 / (W * H * mu) * sum(((i - mu)**2 for i in map(I, imgdata)))

print(f"Focus is {F(img)}")
