from time import sleep
from math import sin, pi
from PiicoDev_Unified import *
i2c = PiicoDev_Unified_I2C()

from PiicoDev_RGB import PiicoDev_RGB

i = 0


leds = PiicoDev_RGB()
# leds.setI2Caddr(0x55)
leds.clear()




while True:
# Pulse three LEDs with three separate colours out of sync
    r = round( 255 * (0.5*sin(i) +0.5) )
    g = round( 255 * (0.5*sin((i + 2*pi/3)) +0.5) )
    b = round( 255 * (0.5*sin(i + 4*pi/3) +0.5) )
#     print(r,g,b)
#     buffer = bytes([r,0,0]) + bytes([0,g,0]) + bytes([0,0,b])

    leds.setPixelColor(0,r,0,0)
    leds.setPixelColor(1,0,g,0)
    leds.setPixelColor(2,0,0,b)
    leds.show()
#     print(buffer)
#     i2c.writeto_mem(addr, 0x03, buffer)
    i = (i + 0.1)
    if i > 2*pi:
        i = 0
        
    
#     count = count + 1
#     if count == 127:
#         sleep(0.001)
#         i2c.writeto_mem(addr, 0x0C, bytes([50]))
#     if count == 255:
#         sleep(0.001)
#         i2c.writeto_mem(addr, 0x0C, bytes([255]))
#         count = 0
#     print(count)
#     sleep(0.05)
    
    
#     buffer = bytes([255,0,0]) + bytes([0,255,0]) + bytes([0,0,255])
#     i2c.writeto_mem(addr, 0x03, buffer)
#     print("on")
#     sleep(0.5)
#     buffer = bytes([255,0,0]) + bytes([0,255,0]) + bytes([0,0,255])
#     i2c.writeto_mem(addr, 0x0D, bytes([0x01]))
#     print("off")
#     sleep(0.5)
    
    sleep(0.01)
    
    
    