// Executes when data is received on I2C
// this function is registered as an event, see setup()
void receiveEvent(int numBytesReceived) {
  registerNumber = Wire.read(); // First byte is the register number

  // Begin recording the incoming bytes to the temp memory map.
  // starting with the registerNumber (the first byte received)
  for (uint8_t x = 0 ; x < numBytesReceived - 1 ; x++) {
    uint8_t temp = Wire.read(); //We might record it, we might throw it away
    if ( (x + registerNumber) < sizeof(memoryMap)) {
      //Mask the incoming byte against the read only protected bits
      //Store the result into the register map
      *(registerPointer + registerNumber + x) &= ~*(protectionPointer + registerNumber + x); //Clear this register if needed
      *(registerPointer + registerNumber + x) |= temp & *(protectionPointer + registerNumber + x); //Set requested bits (protected bits masked-out)
    }
  }
  updateFlag = true;
}

void requestEvent(int numBytesRequested) {
  Wire.write((registerPointer + registerNumber), numBytesRequested);
}
