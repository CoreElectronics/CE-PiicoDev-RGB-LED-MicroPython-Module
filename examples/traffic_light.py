from PiicoDev_RGB import PiicoDev_RGB
from PiicoDev_Unified import sleep_ms # Cross-platform compatible sleep function

trafficA = PiicoDev_RGB() # initialise an RGB LED module with default address (all switches OFF)
trafficB = PiicoDev_RGB(id=[1,0,0,0]) # initialise RGB LED module using switch positions (first switch ON, all others OFF)

red = [255,0,0]
amber = [225,165,0]
green = [0,255,0]

while True:
    ### Traffic flows one way
    trafficA.clear(); trafficB.clear()
    trafficA.setPixel(2, green); trafficA.show()
    trafficB.setPixel(0, red); trafficB.show()
    sleep_ms(2000)
    
    ### Transition
    trafficA.clear();
    trafficA.setPixel(1, amber); trafficA.show()
    sleep_ms(1000)
    
    ### Traffic flows the other way
    trafficA.clear(); trafficB.clear()
    trafficA.setPixel(0, red); trafficA.show()
    trafficB.setPixel(2, green); trafficB.show()
    sleep_ms(2000)
    
    ### Transition
    trafficB.clear();
    trafficB.setPixel(1, amber); trafficB.show()
    sleep_ms(1000)
    