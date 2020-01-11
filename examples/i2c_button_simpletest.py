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
#
# This library based upon Sparkfun's Arduino library and firmware sources:
# github.com/sparkfun/SparkFun_Qwiic_Button_Arduino_Library/blob/master/src
# github.com/sparkfunX/Qwiic_Switch/blob/master/Firmware/Qwiic_Button
"""
`i2c_button_simpletest`
================================================================================

Demonstrate I2C Button (ala Sparkfun Qwiic Button/Switch/Arcade)


* Author(s): Gregory M Paris

Implementation Notes
--------------------

**Hardware:**

    * `Sparkfun Qwiic Button - Red SPX-15584: https://www.sparkfun.com/products/15584`_
    * `Sparkfun Qwiic Button - Blue SPX-15585: https://www.sparkfun.com/products/15585`_
    * `Sparkfun Qwiic Switch SPX-15586: https://www.sparkfun.com/products/15586`_
    * `Sparkfun Qwiic Arcade - Red SPX-15591: https://www.sparkfun.com/products/15591`_
    * `Sparkfun Qwiic Arcade - Blue SPX-15592: https://www.sparkfun.com/products/15592`_

**Software and Dependencies:**

    * Adafruit CircuitPython firmware for the supported boards:
    https://github.com/adafruit/circuitpython/releases

    * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

# imports
import board
import busio
import time
from random import randint
from i2c_button import I2C_Button

# initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# scan the I2C bus for devices
while not i2c.try_lock():
    pass
devices = i2c.scan()
i2c.unlock()
print('I2C devices found:', [hex(n) for n in devices])
default_addr = 0x6f
if default_addr not in devices:
    print('warning: no device at the default button address', default_addr)

# initialize the button
button = I2C_Button(i2c)

# print some stuff
print('firmware version', button.version)
print('interrupts', button.interrupts)
print('debounce ms', button.debounce_ms)

# demonstrate writing to registers
button.led_bright = randint(0, 255)
button.led_gran = randint(0, 1)
button.led_cycle_ms = randint(250, 2000)
button.led_off_ms = randint(100, 500)

# demonstrate reading those registers
print('LED brightness', button.led_bright)
print('LED granularity', button.led_gran)
print('LED cycle ms', button.led_cycle_ms)
print('LED off ms', button.led_off_ms)

# demonstrate button behavior
while True:
    button.clear() # status must be cleared manually
    time.sleep(1)
    print('status', button.status)
    print('last click ms', button.last_click_ms)
    print('last press ms', button.last_press_ms)

