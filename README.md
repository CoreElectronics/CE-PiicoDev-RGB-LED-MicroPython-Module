# PiicoDev® RGB LED MicroPython Module and Firmware

This is the firmware repo for the [Core Electronics PiicoDev® 3x RGB LED Module](https://core-electronics.com.au/catalog/product/view/sku/CE07910)

This module depends on the [PiicoDev Unified Library](https://github.com/CoreElectronics/CE-PiicoDev-Unified), include `PiicoDev_Unified.py` in the project directory on your MicroPython device.


See the [Quickstart Guide](https://piico.dev/p13)

# Details
### `PiicoDev_RGB(bus=, freq=, sda=, scl=, addr=0x08, id=, bright=50):`
Parameter | Type | Range            | Default                               | Description
--------- | ---- | ---------------- | ------------------------------------- | --------------------------------------------------
bus       | int  | 0, 1             | Raspberry Pi Pico: 0, Raspberry Pi: 1 | I2C Bus.  Ignored on Micro:bit
freq      | int  | 100-1000000      | Device dependent                      | I2C Bus frequency (Hz).  Ignored on Raspberry Pi
sda       | Pin  | Device Dependent | Device Dependent                      | I2C SDA Pin. Implemented on Raspberry Pi Pico only
scl       | Pin  | Device Dependent | Device Dependent                      | I2C SCL Pin. Implemented on Raspberry Pi Pico only
addr      | int  | 0x08-0x77        | 0x08                                  | The I2C address of the connected device.
id        | list | [0,0,0,0] to [1,1,1,1] |                                 | A 4-element list of ones or zeros that defines the ID switch configuration. This abstracts the device I2C address - the id argument must match the physical switch states.
bright    | int  | 0-255            | 50                                    | A global scaler for brightness

### `PiicoDev_RGB.setPixel(n, c)`
Set LED `n` to the colour `c`. Changes are not displayed until `PiicoDev_RGB.show()` is called.

Parameter | Type | Range                  | Description
--------- | ---- | ---------------------- |--------------------------------------------------
n         | int  | 0-2                    | The LED number to set. zero-indexed
c         | list | [0-255, 0-255, 0-255]  | R,G,B colour data

### `PiicoDev_RGB.show()`
Sends the LED data to the RGB Module for immediate display.

### `PiicoDev_RGB.fill(c)`
Set all LEDs to the colour `c`. Automatically calls `PiicoDev_RGB.show()`.

### `PiicoDev_RGB.clear(c)`
Blanks all the LEDs.

### `wheel(h,s=1,v=1)`
Pick a colour from the colour wheel. Returns a list `[R,G,B]`

### `PiicoDev_RGB.setBrightness(bright)`
Parameter | Type | Range                  | Description
--------- | ---- | ---------------------- |--------------------------------------------------
bright     | int  | 0-255                 | Update the global brightness scaler

### `PiicoDev_RGB.pwrLED(state)`
The on-board green LED functions as a power LED - it is always on by default. It can be disabled with this function.

Parameter | Type | Range                  | Description
--------- | ---- | ---------------------- |--------------------------------------------------
state     | int  | True/1, False/0    | Enable / Disable the LED


# License
This project is open source - please review the LICENSE.md file for further licensing information.

If you have any technical questions, or concerns about licensing, please contact technical support on the [Core Electronics forums](https://forum.core-electronics.com.au/).

# Attribution
C++ code firmware project is based off the [Qwiic Switch](https://github.com/sparkfunX/Qwiic_Switch) project by Sparkfun. It makes use of the register structure and i2c device drivers.

*\"PiicoDev\" and the PiicoDev logo are trademarks of Core Electronics Pty Ltd.*
