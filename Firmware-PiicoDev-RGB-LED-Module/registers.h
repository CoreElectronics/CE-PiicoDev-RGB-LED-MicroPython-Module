/******************************************************************************
  registers.h
  Michael Ruppe @ Core Electronics
  June 2021

  Based off the work by
  Fischer Moseley @ SparkFun Electronics
  Original Creation Date: July 31, 2019

  This file defines the memoryMap struct, which acts as the virtual register map
  of the PiicoDev GlowBit Module. It also serves as an easy way to access variables
  and manipulate the state of the device.

  During I2C transactions, the memoryMap object is wrapped as a collection of
  bytes. The byte that the user is interested in (either to read or write) is
  selected with a register pointer. For instance, if the user sets the pointer
  to 0x0C, they will be addressing the 12th uint8_t sized object in this struct.
  In this case, that would be the ledBrightness register!

  Distributed as-is; no warranty is given.
******************************************************************************/

typedef struct memoryMap {
  //Device status/configuration               Register Address
  uint8_t id;                               // 0x00
  uint8_t firmwareMinor;                    // 0x01
  uint8_t firmwareMajor;                    // 0x02

  // Control register. Use to issue commands to power LED or to clear RGB LEDs
  uint8_t pwrLedCtrl;                       // 0x03
  uint8_t clearLeds;                        // 0x04
  
  //Device Configuration
  uint8_t i2cAddress;                       // 0x05

  //LED Configuration
  uint8_t ledBrightness;                    // 0x06
  uint8_t ledValues[9];                     // 0x07
};
// ledValues is the last entry in the register map - if more LEDs are desired
// the register map can simply expand to accommodate
