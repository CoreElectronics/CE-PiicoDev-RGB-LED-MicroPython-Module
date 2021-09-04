from time import sleep
from math import sin, pi
from PiicoDev_Unified import *
i2c = PiicoDev_Unified_I2C()

from PiicoDev_RGB import PiicoDev_RGB, hsv_to_rgb

i = 0


leds = PiicoDev_RGB(0x20)
# leds.setI2Caddr(0x55)
leds.clear()
sleep(0.1)

leds.setBrightness(20)

while True:
    c = hsv_to_rgb(i/360)
    leds.fill(c)
    i = i + 1
    i = i%360
    sleep(0.005)
    
    
#     leds.fill([255,0,0]); leds.show()
#     sleep(0.5)
#     leds.fill([0,255,0])
#     sleep(0.5)
#     leds.fill([0,0,255])
#     sleep(0.5)
# Pulse three LEDs with three separate colours out of sync
#     r = round( 255 * (0.5*sin(i) +0.5) )
#     g = round( 255 * (0.5*sin((i + 2*pi/3)) +0.5) )
#     b = round( 255 * (0.5*sin(i + 4*pi/3) +0.5) )
# 
# 
#     leds.setPixelColor(0,r,0,0)
#     leds.setPixelColor(1,0,g,0)
#     leds.setPixelColor(2,0,0,b)
#     leds.show()
# 
#     i = (i + 0.1)
#     if i > 2*pi:
#         i = 0
#             
#     sleep(0.01)


#     leds.setPixelColor(0,20,0,0)
#     leds.show()
#     sleep(0.25)
#     leds.clear()
#     sleep(0.25)



    
    