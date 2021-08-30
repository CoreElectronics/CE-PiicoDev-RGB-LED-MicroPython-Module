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
typedef union {
  struct {
    bool clearLedFlag : 1; // This is bit 0. User mutable, set to 1 will clear all leds (for the .clear() command)
    bool pwrLedCtl : 1;    // Enable (1) or Disable (0) the Power LED
    bool : 6;              // pad the remaining bits to next whole byte
  };
  uint8_t wrapperByte;
} controlRegisterBitField;


typedef struct memoryMap {
  //Device status/configuration               Register Address
  uint8_t id;                               // 0x00
  uint8_t firmwareMinor;                    // 0x01
  uint8_t firmwareMajor;                    // 0x02

  // Control register. Use to issue commands. So far only bit0 is used: set bit0 to clear all LEDs
  controlRegisterBitField control;          // 0x03

  //Device Configuration
  uint8_t i2cAddress;                       // 0x04

  //LED Configuration
  uint8_t ledBrightness;                    // 0x05
  uint8_t ledValues[9];                     // 0x06
};
// ledValues is the last entry in the register map - if more LEDs are desired
// the register map can simply expand to accommodate
