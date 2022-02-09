/*
 * PiicoDev 3x RGB LED Module Firmware
 * Written by Michael Ruppe @ Core Electronics
 * Based off the Qwiic Button Project https://github.com/sparkfun/Qwiic_Button
 * Date: NOV 2021
 * An I2C based LED module that allows control of 3x GlowBit (WS2812) LEDs
 * 
 * Feel like supporting PiicoDev? Buy a module here: https://core-electronics.com.au/catalog/product/view/sku/CE07910
 */

//#define DEBUG
#define F_CPU 8000000
#include <Wire.h>
#include <EEPROM.h>
#include <stdint.h>
#include <tinyNeoPixel_Static.h>
#include <avr/sleep.h> // For sleep_mode
#include <avr/power.h> // For powering-down peripherals such as ADC and Timers
#include "registers.h" // Defines this devices virtual registers
#include "nvm.h"       // EEPROM locations

#define FIRMWARE_MAJOR 0x01
#define FIRMWARE_MINOR 0x01

#define DEVICE_ID 0x84
#define DEFAULT_I2C_ADDRESS 0x08 // Works best if second digit is always zero - so address jumpers may set incrementing address always
#define SOFTWARE_ADDRESS true
#define HARDWARE_ADDRESS false
uint8_t oldAddress;

// Hardware Connections ATtiny8x6, ATtiny16x6
const uint8_t powerLedPin = PIN_PC2;
const uint16_t glowbitPin = PIN_PA1;

const uint8_t addressPin1 = PIN_PA7;
const uint8_t addressPin2 = PIN_PB5;
const uint8_t addressPin3 = PIN_PA5;
const uint8_t addressPin4 = PIN_PB2;

const int NUMLEDS = 3;
byte glowbits[NUMLEDS * 3];
tinyNeoPixel leds = tinyNeoPixel(NUMLEDS, glowbitPin, NEO_GRB, glowbits);

volatile uint8_t brightness = 255; // LED brightness scaler
uint8_t oldBrightness = 0xFF;
volatile bool updateFlag = true; // Goes true when new data received. Cause LEDs to update

// Global variables
// *****************************************************************************
// Defaults for all settings

// Initialise the virtual I2C registers
volatile memoryMap registerMap {
  DEVICE_ID,            //id
  FIRMWARE_MINOR,       //firmwareMinor
  FIRMWARE_MAJOR,       //firmwareMajor
  0x01,                  //power LED state
  0x00,                  //clear-rgb-leds command
  DEFAULT_I2C_ADDRESS,  //i2cAddress
  255,                  //ledBrightness
  {0, 0, 0, 0, 0, 0, 0, 0, 0} //ledValues
};

// Define which registers are user-modifiable. (0 = protected, 1 = modifiable)
volatile memoryMap protectionMap {
  0x00,                                             //id
  0x00,                                             //firmwareMinor
  0x00,                                             //firmwareMajor
  0xFF,
  0xFF,
  0xFF,                                             //i2cAddress
  0xFF,                                             //ledBrightness
  {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF} //ledValues
};


//Cast 32bit address of the object registerMap with uint8_t so we can increment the pointer
uint8_t *registerPointer = (uint8_t *)&registerMap;
uint8_t *protectionPointer = (uint8_t *)&protectionMap;
volatile uint8_t registerNumber; //Gets set when user writes an address. We then serve the spot the user requested.



void setup() {
  // Pull up address pins
  pinMode(addressPin1, INPUT_PULLUP);
  pinMode(addressPin2, INPUT_PULLUP);
  pinMode(addressPin3, INPUT_PULLUP);
  pinMode(addressPin4, INPUT_PULLUP);
  pinMode(powerLedPin, OUTPUT);
  powerLed(true); // enable Power LED by default on ever power-up

  pinMode(glowbitPin, OUTPUT);
#ifdef DEBUG
  leds.setPixelColor(0, 255, 0, 0); // first LED full RED
  leds.show();                   // LED turns on.
  delay(1000);
#endif

  // squash spurious WS2812 LED power-on behaviour
  delay(1); leds.clear(); leds.show();

  //  Serial.pins(PIN_PA1, PIN_PA2);  // For Xplained Nano breakout
  //  Serial.begin(9600);             // For Xplained Nano breakout
  //  Serial.println("Begin");


  set_sleep_mode(SLEEP_MODE_IDLE);
  sleep_enable();
  readSystemSettings(&registerMap); //Load all system settings from EEPROM

  startI2C(&registerMap);          //Determine the I2C address we should be using and begin listening on I2C bus
  oldAddress = registerMap.i2cAddress;

}

void loop() {
  // Check to see if the I2C address has been updated by software, set the appropriate address-type flag
  if (oldAddress != registerMap.i2cAddress)
  {
    oldAddress = registerMap.i2cAddress;
    EEPROM.put(LOCATION_ADDRESS_TYPE, SOFTWARE_ADDRESS);
    startI2C(&registerMap);
  }

  if (updateFlag) {
    // Clear LEDs
    if (registerMap.clearLeds == 1) {
      registerMap.clearLeds = 0;
      memset(registerMap.ledValues, 0, sizeof(registerMap.ledValues) ); // dump all led values
      leds.clear(); leds.show();
    }

    // Power LED - open drain so toggle between output-low and high-impedance input
    static bool lastPowerLed = true;
    if (registerMap.pwrLedCtrl != lastPowerLed) {
      lastPowerLed = registerMap.pwrLedCtrl;
      powerLed(registerMap.pwrLedCtrl);
    }

    // GlowBit brightness
    if (oldBrightness != registerMap.ledBrightness) {
      leds.setBrightness(registerMap.ledBrightness);
      oldBrightness = registerMap.ledBrightness;
    }

    // write buffer data to each LED
    // LEDs are updated on every updateFlag - it's implicit that this is the most used function so... why not?
    leds.setPixelColor(0, registerMap.ledValues[0], registerMap.ledValues[1], registerMap.ledValues[2] );
    leds.setPixelColor(1, registerMap.ledValues[3], registerMap.ledValues[4], registerMap.ledValues[5] );
    leds.setPixelColor(2, registerMap.ledValues[6], registerMap.ledValues[7], registerMap.ledValues[8] );
    leds.show();

    //Record anything new to EEPROM (like new i2c address)
    //It can take a handful of ms to write a byte to EEPROM so we do that here instead of in an interrupt
    recordSystemSettings(&registerMap);
    updateFlag = false;
  }

  sleep_mode();
}

//Update own I2C address to what's configured with registerMap.i2cAddress and/or the address jumpers.
void startI2C(memoryMap *map)
{
  uint8_t address;
  uint8_t addressType;
  EEPROM.get(LOCATION_ADDRESS_TYPE, addressType);

  if (addressType == 0xFF)
  {
    EEPROM.put(LOCATION_ADDRESS_TYPE, SOFTWARE_ADDRESS);
  }

  // Add hardware address jumper values to the default address
  uint8_t IOaddress = DEFAULT_I2C_ADDRESS;
  uint8_t switchPositions = 0;
  bitWrite(switchPositions, 0, !digitalRead(addressPin1));
  bitWrite(switchPositions, 1, !digitalRead(addressPin2));
  bitWrite(switchPositions, 2, !digitalRead(addressPin3));
  bitWrite(switchPositions, 3, !digitalRead(addressPin4));
  IOaddress += switchPositions;

  //If any of the address jumpers are set, we use jumpers
  if ((IOaddress != DEFAULT_I2C_ADDRESS) || (addressType == HARDWARE_ADDRESS))
  {
    address = IOaddress;
    EEPROM.put(LOCATION_ADDRESS_TYPE, HARDWARE_ADDRESS);
  }
  //If none of the address jumpers are set, we use registerMap (but check to make sure that the value is legal first)
  else
  {
    //if the value is legal, then set it
    if (map->i2cAddress > 0x07 && map->i2cAddress < 0x78)
      address = map->i2cAddress;

    //if the value is illegal, default to the default I2C address for our platform
    else
      address = DEFAULT_I2C_ADDRESS;
  }

  //save new address to the register map
  map->i2cAddress = address;

  //reconfigure Wire instance
  Wire.end();          //stop I2C on old address
  Wire.begin(address); //rejoin the I2C bus on new address

  //The connections to the interrupts are severed when a Wire.begin occurs, so here we reattach them
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
}


// Control the power LED - open drain output so toggle between enable (output, low) and disable (high-impedance input)
void powerLed(bool enable) {
  if (enable) {
    pinMode(powerLedPin, OUTPUT);
    digitalWrite(powerLedPin, HIGH);
  } else {
    pinMode(powerLedPin, INPUT);
  }
}
