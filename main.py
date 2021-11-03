from PiicoDev_RGB import PiicoDev_RGB, wheel
from PiicoDev_Unified import sleep_ms # Cross-platform compatible sleep function

leds = PiicoDev_RGB() # initialise the LED module with conservative default brightness
# leds.setBrightness(127) # 0-255 set the global brightness to half

# Set LED# to pure Red, Green, Blue
leds.setPixel(0, 255,0,0) # 0: red
leds.setPixel(1, 0,255,0) # 1: green
leds.setPixel(2, 0,0,255) # 2: blue
leds.show()
sleep_ms(2000)
leds.clear() # clear the LEDs
sleep_ms(1000)

i = 0 # loop counter
powerLedState = True # LED state

while True:
    c = wheel(i/360) # pick a colour from the colour wheel
    leds.fill(c) # fill() will automatically show()
    
    if i % 100 == 0: # every 100 loops toggle the power LED
        powerLedState = not powerLedState # toggle state variable
        leds.pwrLED(powerLedState) # update power LED       
    
    i = i+1
    sleep_ms(5)
