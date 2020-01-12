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
`i2c_button_change_address`
================================================================================

Demo changing the I2C address of a Sparkfun Qwiic Button/Switch/Arcade

* Author(s): Gregory M Paris
"""

# imports
import board
import busio
from i2c_button import I2C_Button

DEF_ADDR = 0x6f
NEW_ADDR = 0x60

# initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# make sure we're not going to cause a conflict
while not i2c.try_lock():
    pass
collision = NEW_ADDR in i2c.scan()
i2c.unlock()
if collision:
    print('there is already a device at address', hex(NEW_ADDR))
    exit()

# initialize the button at the default I2C address
button = I2C_Button(i2c, DEF_ADDR)
print('found button at', hex(button.i2c_addr))

# change the address
# once this happens, the button object is broken
button.i2c_addr = NEW_ADDR

# initialize at the new address
button = I2C_Button(i2c, NEW_ADDR)
print('button now at', hex(button.i2c_addr))

# put it back to default
button.i2c_addr = DEF_ADDR
button = I2C_Button(i2c, DEF_ADDR)
print('button restored to address', hex(button.i2c_addr))
