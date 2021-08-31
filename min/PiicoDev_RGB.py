from PiicoDev_Unified import *
from time import sleep
i2c=PiicoDev_Unified_I2C()
_baseAddr=8
_DevID=132
_regDevID=0
_regFirmVer=1
_regCtrl=3
_regI2cAddr=4
_regBright=5
_regLedVals=6
class PiicoDev_RGB:
	def setPixelColor(self,n,r,g,b):self.led[n]=[r,g,b]
	def show(self):buffer=bytes(self.led[0])+bytes(self.led[1])+bytes(self.led[2]);i2c.writeto_mem(self.addr,_regLedVals,buffer)
	def setBrightness(self,x):self.bright=x;self.i2c.writeto_mem(self.addr,_regBright,bytes([self.bright]));sleep(0.001)
	def clear(self):self.i2c.writeto_mem(self.addr,_regCtrl,bytes([1]));sleep(0.001)
	def setI2Caddr(self,newAddr):
		if newAddr>=8 and newAddr<=119:self.i2c.writeto_mem(self.addr,_regI2cAddr,bytes([newAddr]));self.addr=newAddr
		else:print('address must be >=0x08 and <=0x77')
	def readFirmware(self):v=self.i2c.readfrom_mem(self.addr,_regFirmVer,2);return v[1],v[0]
	def readID(self):return self.i2c.readfrom_mem(self.addr,_regDevID,1)[0]
	def pwrLED(self,bit):
		if bit==False:b=0
		else:b=1
		self.i2c.writeto_mem(self.addr,_regCtrl,bytes([b<<1]))
	def __init__(self,addr=_baseAddr,i2c=i2c,bright=50):
		self.i2c=i2c;a=addr
		if type(a)is list:self.addr=_baseAddr+a[0]+2*a[1]+4*a[2]+8*a[3]
		else:self.addr=a
		self.led=[[0,0,0],[0,0,0],[0,0,0]];self.bright=bright
		try:
			if self.readID()!=_DevID:print('* Incorrect device found at address {}'.format(addr))
			self.setBrightness(bright);self.show()
		except:print("* Couldn't find a device - check switches and wiring")