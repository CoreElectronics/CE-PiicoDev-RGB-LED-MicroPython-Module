from math import sin, pi
from PiicoDev_RGB import PiicoDev_RGB, hsv_to_rgb
from PiicoDev_Unified import sleep_ms # Cross-platform compatible sleep function

leds = PiicoDev_RGB(addr=0x77) # initialise the LED module
leds.setBrightness(20) # set the global brightness

print("ID: ",leds.readID())
print("ver. ",leds.readFirmware())


leds.setI2Caddr(0x08)
leds.setPixel(0,20.5,100,255)
leds.show()
while True:
    sleep_ms(1)
i = 0 # loop counter
x = 1 # LED state
while True:
    c = hsv_to_rgb(i/360)
    leds.fill(c)
    i = i + 1
    i = i%360
    
    i = i+1
    if i % 100 == 0:
        leds.pwrLED(x)
        if x == 1:
            x = 0
        else:
            x = 1
    sleep_ms(5)
    
    
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



    
    