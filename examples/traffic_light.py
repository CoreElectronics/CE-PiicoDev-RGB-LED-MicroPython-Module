from PiicoDev_RGB import PiicoDev_RGB
from PiicoDev_Unified import sleep_ms # Cross-platform compatible sleep function

traffic1 = PiicoDev_RGB() # initialise an RGB LED module with default address (all switches OFF)
traffic2 = PiicoDev_RGB(id=[1,0,0,0]) # initialise RGB LED module using switch positions (first switch ON, all others OFF)

# These functions set the corresponding RGB LED module to  a given colour
def Red(module):
    module.clear();
    module.setPixel(0,255,0,0) # top light red
    module.show()
    
def Amber(module):
    module.clear();
    module.setPixel(1,255,165,0) # middle light amber
    module.show()
    
def Green(module):
    module.clear();
    module.setPixel(2,0,255,0) # bottom light green
    module.show()

while True:
    ### Traffic flows one way
    Green(traffic1) 
    Red(traffic2)
    sleep_ms(2000)
    
    ### Transition
    Amber(traffic1)
    sleep_ms(1000)
    
    ### Traffic flows the other way
    Red(traffic1)
    Green(traffic2)
    sleep_ms(2000)
    
    ### Transition
    Amber(traffic2)
    sleep_ms(1000)
    