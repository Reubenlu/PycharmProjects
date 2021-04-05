# -------------------------------------------------
# !/usr/bin/env python
# -*- coding:utf8 -*-
# FileName: 1
# Description :
# Date    : 2021/4/4 16:09
# Author  : {USER}/Reuben.Lu
# -------------------------------------------------
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
RST = 17
DC = 22
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_64(rst=str(RST), dc=str(DC), spi=SPI.SpiDev(0, 0, max_speed_hz=800000))
disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
image1 = Image.new('1', (width, height))
draw1 = ImageDraw.Draw(image1)
padding = 1
shape_width = 50
left = padding
top = padding
right = width-padding
bottom = height-padding
x = padding
draw1.rectangle((left, top, right, bottom), outline=1, fill=0)
draw1.ellipse((left+10, top+10, left+10+shape_width, top+10+shape_width), outline=1, fill=0)
draw1.polygon([(right-20, top+10), (width/2+5, bottom-10), (right-5, bottom-10)], outline=1, fill=0)


image2 = Image.open('testImage.jpg').resize((128, 64)).convert('1')


image3 = Image.new('1', (width, height))
draw3 = ImageDraw.Draw(image3)
font1 = ImageFont.load_default()
font2 = ImageFont.truetype('04B_30__.TTF', 15)
font3 = ImageFont.truetype('baby blocks.ttf', 18)
draw3.text((0, 0), 'Hello', font=font1, fill=1)
draw3.text((0, 15), 'World!', font=font2, fill=1)
draw3.text((0, 35), 'Enjoy it!', font=font3, fill=1)
# ----------------------------------------------------------------------------------------------------------

try:
    index = 1
    while True:
        if index == 1:
            disp.image(image1)
            index += 1
        elif index == 2:
            disp.image(image2)
            index += 1
        else:
            disp.image(image3)
            index = 1
        disp.display()
        time.sleep(2)
except:
    disp.clear()
    disp.display()
