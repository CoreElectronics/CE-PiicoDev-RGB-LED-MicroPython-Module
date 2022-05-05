_A=None
from PiicoDev_Unified import *
_baseAddr=8
_DevID=132
_regDevID=0
_regFirmVer=1
_regCtrl=3
_regClear=4
_regI2cAddr=5
_regBright=6
_regLedVals=7
def wheel(h,s=1,v=1):
	A=1.0
	if s==0.0:v*=255;return v,v,v
	i=int(h*6.0);f=h*6.0-i;p,q,t=int(255*(v*(A-s))),int(255*(v*(A-s*f))),int(255*(v*(A-s*(A-f))));v*=255;i%=6
	if i==0:return[v,t,p]
	if i==1:return[q,v,p]
	if i==2:return[p,v,t]
	if i==3:return[p,q,v]
	if i==4:return[t,p,v]
	if i==5:return[v,p,q]
class PiicoDev_RGB:
	def setPixel(self,n,c):self.led[n]=[round(c[0]),round(c[1]),round(c[2])]
	def show(self):buffer=bytes(self.led[0])+bytes(self.led[1])+bytes(self.led[2]);self.i2c.writeto_mem(self.addr,_regLedVals,buffer)
	def setBrightness(self,x):self.bright=round(x)if 0<=x<=255 else 255;self.i2c.writeto_mem(self.addr,_regBright,bytes([self.bright]));sleep_ms(1)
	def clear(self):self.i2c.writeto_mem(self.addr,_regClear,b'\x01');self.led=[[0,0,0],[0,0,0],[0,0,0]];sleep_ms(1)
	def setI2Caddr(self,newAddr):x=int(newAddr);assert 8<=x<=119,'address must be >=0x08 and <=0x77';self.i2c.writeto_mem(self.addr,_regI2cAddr,bytes([x]));self.addr=x;sleep_ms(5)
	def readFirmware(self):v=self.i2c.readfrom_mem(self.addr,_regFirmVer,2);return v[1],v[0]
	def readID(self):return self.i2c.readfrom_mem(self.addr,_regDevID,1)[0]
	def pwrLED(self,state):assert state==True or state==False,'argument must be True/1 or False/0';self.i2c.writeto_mem(self.addr,_regCtrl,bytes([state]));sleep_ms(1)
	def fill(self,c):
		for i in range(len(self.led)):self.led[i]=c
		self.show()
	def __init__(self,bus=_A,freq=_A,sda=_A,scl=_A,addr=_baseAddr,id=_A,bright=50):
		self.i2c=create_unified_i2c(bus=bus,freq=freq,sda=sda,scl=scl)
		if type(id)is list:assert max(id)<=1 and min(id)>=0 and len(id)is 4,'id must be a list of 1/0, length=4';self.addr=_baseAddr+id[0]+2*id[1]+4*id[2]+8*id[3]
		else:self.addr=addr
		self.led=[[0,0,0],[0,0,0],[0,0,0]];self.bright=bright
		try:self.setBrightness(bright);self.show()
		except Exception as e:print("* Couldn't find a device - check switches and wiring");raise e