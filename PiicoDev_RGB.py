from PiicoDev_Unified import *
i2c=PiicoDev_Unified_I2C()
_baseAddr=0x20
_DevID=0x84
_regDevID=0x00
_regFirmVer=0x01
_regCtrl=0x03
_regI2cAddr=0x04
_regBright=0x05
_regLedVals=0x06

def hsv_to_rgb(h, s=1, v=1):
    if s == 0.0: v*=255; return (v, v, v)
    i = int(h*6.) # XXX assume int() truncates!
    f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
    if i == 0: return [v, t, p]
    if i == 1: return [q, v, p]
    if i == 2: return [p, v, t]
    if i == 3: return [p, q, v]
    if i == 4: return [t, p, v]
    if i == 5: return [v, p, q]

class PiicoDev_RGB(object):
    def setPixelColor(self,n,r,g,b):
        self.led[n]=[r,g,b]
    def show(self):
        buffer = bytes(self.led[0]) + bytes(self.led[1]) + bytes(self.led[2])
        i2c.writeto_mem(self.addr, _regLedVals, buffer)
    def setBrightness(self,x):
        self.bright=x
        self.i2c.writeto_mem(self.addr, _regBright, bytes([self.bright]))
        sleep_ms(1)
    def clear(self):
        d=self.i2c.readfrom_mem(self.addr, _regCtrl, 1)
        r=int.from_bytes(d,'big')
        sleep_ms(1)
        r|=(1<<0) # zero-th bit is the clear flag
        self.i2c.writeto_mem(self.addr,_regCtrl,bytes([r]))
        sleep_ms(1)
    def setI2Caddr(self, newAddr):
        if newAddr >= 0x08 and newAddr <= 0x77: #check valid address
            self.i2c.writeto_mem(self.addr, _regI2cAddr, bytes([newAddr]))
            self.addr = newAddr
            sleep_ms(5)
        else:
            print('address must be >=0x08 and <=0x77')
    def readFirmware(self):
        v=self.i2c.readfrom_mem(self.addr, _regFirmVer, 2)
        return (v[1],v[0])
    def readID(self):
        return self.i2c.readfrom_mem(self.addr, _regDevID, 1)[0]
    def pwrLED(self,bit):
        d=self.i2c.readfrom_mem(self.addr, _regCtrl, 1)
        d=int.from_bytes(d,'big')
        sleep_ms(1)
        if bit == False:
            d&=~(1<<1) # 1th bit is the pwrLED
        else:
            d|=(1<<1)
        self.i2c.writeto_mem(self.addr,_regCtrl,bytes([d]))
        sleep_ms(1)
    def fill(self,c):
        for i in range(len(self.led)):
            self.led[i]=c
        self.show()
    def __init__(self, addr=_baseAddr, i2c=i2c, bright=50):
        self.i2c = i2c
        a=addr
        if type(a) is list:
            self.addr=_baseAddr+a[0]+2*a[1]+4*a[2]+8*a[3]
        else:
            self.addr = a            
        self.led = [[0,0,0],[0,0,0],[0,0,0]]
        self.bright=bright
        try:
            if self.readID() != _DevID:
                print("* Incorrect device found at address {}".format(addr))
            self.setBrightness(bright)
            self.show()
        except:
            print("* Couldn't find a device - check switches and wiring")
        
        