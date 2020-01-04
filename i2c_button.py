# The MIT License (MIT)
#
# Copyright (c) 2020 Gregory M Paris
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`i2c_button`
================================================================================

I2C Button ala Sparkfun Qwiic Arcade Button


* Author(s): Gregory M Paris

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s). Use unordered list & hyperlink rST
   inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports
from adafruit_bus_device.i2c_device import I2CDevice

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/gmparis/CircuitPython_i2c_button.git"

# Register values and data format from
#    github.com/sparkfun/SparkFun_Qwiic_Button_Arduino_Library/blob/master/src/registers.h
# //Register Pointer Map
# enum Qwiic_Button_Register : uint8_t
# {
#     ID = 0x00,
#     FIRMWARE_MINOR = 0x01,
#     FIRMWARE_MAJOR = 0x02,
#     BUTTON_STATUS = 0x03,
#     INTERRUPT_CONFIG = 0x04,
#     BUTTON_DEBOUNCE_TIME = 0x05,
#     PRESSED_QUEUE_STATUS = 0x07,
#     PRESSED_QUEUE_FRONT = 0x08,
#     PRESSED_QUEUE_BACK = 0x0C,
#     CLICKED_QUEUE_STATUS = 0x10,
#     CLICKED_QUEUE_FRONT = 0x11,
#     CLICKED_QUEUE_BACK = 0x15,
#     LED_BRIGHTNESS = 0x19,
#     LED_PULSE_GRANULARITY = 0x1A,
#     LED_PULSE_CYCLE_TIME = 0x1B,
#     LED_PULSE_OFF_TIME = 0x1D,
#     I2C_ADDRESS = 0x1F,
# };
#
# typedef union {
#     struct
#     {
#         bool eventAvailable : 1; //This is bit 0. User mutable, gets set to 1 when a new event occurs. User is expected to write 0 to clear the flag.
#         bool hasBeenClicked : 1; //Defaults to zero on POR. Gets set to one when the button gets clicked. Must be cleared by the user.
#         bool isPressed : 1;      //Gets set to one if button is pushed.
#         bool : 5;
#     };
#     uint8_t byteWrapped;
# } statusRegisterBitField;
#
# typedef union {
#     struct
#     {
#         bool popRequest : 1; //This is bit 0. User mutable, user sets to 1 to pop from queue, we pop from queue and set the bit back to zero.
#         bool isEmpty : 1;    //user immutable, returns 1 or 0 depending on whether or not the queue is empty
#         bool isFull : 1;     //user immutable, returns 1 or 0 depending on whether or not the queue is full
#         bool : 5;
#     };
#     uint8_t byteWrapped;
# } queueStatusBitField;

class I2C_Button():
    """I2C-connected button, e.g., Sparkfun Qwiic Arcade Button

        :param i2c_obj: existing I2C object
        :param i2c_addr: I2C address of the Qwiic button
        :param dev_id: Device ID of the Qwiic button
    """
    DEFAULT_ADDRESS = 0x1f
    DEV_ID = 0x5d

    def __init__(self, i2c_obj, i2c_addr=DEFAULT_ADDRESS, dev_id=DEV_ID):
        self.i2c = i2c_obj
        self.i2c_addr = i2c_addr
        self.dev_id = dev_id
        self.device = I2CDevice(i2c_obj, i2c_addr)

    def is_connected(self):
        """True if the button is connected and has the expected device ID."""
        return False

    def read_reg(self, register, numbytes=1):
        "Write the regsister number, read back the value."""
        regid = bytearray(1)
        regid[1] = register
        buf = bytearray(numbytes)
        self.device.write_then_readinto(regid, buf)
        return int.from_bytes(buf, byteorder='big', signed=False)

