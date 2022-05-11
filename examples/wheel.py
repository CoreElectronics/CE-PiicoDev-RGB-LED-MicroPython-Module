# Pick a colour from the colour wheel.

from PiicoDev_RGB import PiicoDev_RGB, wheel
from PiicoDev_Unified import sleep_ms # Cross-platform compatible sleep function

leds = PiicoDev_RGB() # initialise the LED module with conservative default brightness

x = 0
while True:
    colour = wheel(x)
    leds.fill( colour )
    x += 0.005
    sleep_ms(20)