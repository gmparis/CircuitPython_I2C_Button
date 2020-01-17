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
`i2c_button_polling`
================================================================================

Demonstrate Polling of CircuitPython I2C Buttons


* Author(s): Gregory M Paris
"""

# imports
import time
import board
import busio
from i2c_button import I2C_Button

# addresses
ADDRS = (0x6e, 0x6f) # as many buttons as you have!

# initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)
# initialize the buttons
buttons = []
for bid, addr in enumerate(ADDRS):
    btn = I2C_Button(i2c, addr, name='btn'+str(bid))
    buttons.append(btn)
    btn.debounce_ms = 25 # default is 10 ms, but it seems too short
    btn.led_bright = btn.led_gran = 0
    btn.led_cycle_ms = btn.led_off_ms = 0

def clear_all():
    """Clear status of all buttons."""
    for cbtn in buttons:
        cbtn.clear()

# In this example, the LED associated with each button should light
# if that button was the first one pressed in the round. (Sort of.)
clear_all()
while True:
    # Next line, sleep time should be longer than debounce time.
    # However, the best reason for using an I2C button is to avoid
    # a tight button-polling loop, so let's use a big sleep here.
    time.sleep(0.500)
    clicked = [btn for btn in buttons if btn.status.been_clicked]
    nclicked = len(clicked)
    if nclicked == 0:
        continue
    for btn in buttons:
        btn.led_bright = 0
    if nclicked == 1:
        wbtn = clicked[0]
    else:
        # Winner is the one who *stopped clicking* first.
        # NOTE: Really should check first_click_ms, but dealing with
        # the queue is too confusing for my small mind :)
        # NOTE: This will crash when two buttons have the same last_click_ms,
        # if the sort code is commented out in the I2C_Button definition.
        wbtn = sorted([(btn.last_click_ms, btn) for btn in clicked])[0][1]
    wbtn.led_bright = 255
    print(wbtn.name)
    clear_all()
