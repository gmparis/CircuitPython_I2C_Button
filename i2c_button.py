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
`i2c_button`
================================================================================

I2C Button ala Sparkfun Qwiic Button/Switch/Arcade


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
from adafruit_bus_device.i2c_device import I2CDevice
from collections import namedtuple

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/gmparis/CircuitPython_i2c_button.git"

_ENDIAN = 'little'
_DEF_ADDR = 0x6f
_DEV_ID = 0x5d
# Button status flags and tuple
_BS_EVENT = 0x1 # clear after use
_BS_CLICKED = 0x2 # clear after use
_BS_PRESSED = 0x4 # user immutable
_BS = namedtuple('_BS', ('available', 'been_clicked', 'is_pressed'))
# Interrupt status flags
_INT_CL = 0x1 # enable an interrupt on button click
_INT_PR = 0x2 # enable an interrupt on button press
_INT = namedtuple('_INT', ('on_click', 'on_press'))
# Queue status flags and tuple
_QS_POP = 0x1 # set to pop from queue
_QS_EMPTY = 0x2 # user immutable
_QS_FULL = 0x4 # user immutable
_QS = namedtuple('_QS', ('empty', 'full'))

class ButtonError(Exception):
#   """Button-related error conditions."""
    pass

def _read_register(button, register, n_bytes=1):
#   """Write the register number, read back the value."""
    regid = register.to_bytes(1, _ENDIAN)
    buf = bytearray(n_bytes)
    with button.device as dev:
        dev.write_then_readinto(regid, buf)
    return int.from_bytes(buf, _ENDIAN)

def _write_register(button, register, value, n_bytes=1):
#   """Write the register number, write the value."""
    buf = bytearray(1 + n_bytes)
    buf[0] = register
    buf[1:] = value.to_bytes(n_bytes, _ENDIAN)
#   print('sending ', buf)
    with button.device as dev:
        dev.write(buf)

# Button Register Descriptor class
class _Reg():
    def __init__(self, addr, width, readonly=False):
        self.addr = addr
        self.width = width
        self.readonly = readonly

    def __get__(self, button, objtype):
        return _read_register(button, self.addr, self.width)

    def __set__(self, button, value):
        if self.readonly:
            raise ButtonError('write to read-only register ' + hex(self.addr))
        _write_register(button, self.addr, value, self.width)

class I2C_Button():
    """I2C-connected button, ala Sparkfun Qwiic Button/Switch/Arcade

        :param i2c_obj: initialized I2C object
        :param i2c_addr: I2C address of the button (optional)
        :param dev_id: Device ID of the button (optional)
    """

    def __init__(self, i2c_obj, i2c_addr=_DEF_ADDR, dev_id=_DEV_ID):
        self.i2c = i2c_obj
        self.device = I2CDevice(i2c_obj, i2c_addr)
        if self.dev_id != dev_id:
            raise ButtonError('wrong device 0x%x at address 0x%x' % (self.dev_id, i2c_addr))

    def __repr__(self):
        return '%s(%s, %s, %s)' % (self.__class__.__name__,
                repr(self.i2c), hex(self.i2c_addr), hex(self.dev_id))
    
    # registers
    dev_id = _Reg(0x00, 1, True) # ID (ro)
    _fwmin = _Reg(0x01, 1, True) # FIRMWARE_MINOR (ro)
    _fwmaj = _Reg(0x02, 1, True) # FIRMWARE_MAJOR (ro)
    _bs = _Reg(0x03, 1) # BUTTON_STATUS (see _BS flags above)
    _int = _Reg(0x04, 1) # INTERRUPT_CONFIG (see _INT flags above)
    debounce_ms = _Reg(0x05, 2) # BUTTON_DEBOUNCE_TIME (ms)
    _prqs = _Reg(0x07, 1) # PRESSED_QUEUE_STATUS (see _QS flags above)
    last_press_ms = _Reg(0x08, 4, True) # PRESSED_QUEUE_FRONT (ro) (ms)
    first_press_ms = _Reg(0x0c, 4, True) # PRESSED_QUEUE_BACK (ro) (ms)
    _clqs = _Reg(0x10, 1) # CLICKED_QUEUE_STATUS (see _QS flags above)
    last_click_ms = _Reg(0x11, 4, True) # CLICKED_QUEUE_FRONT (ro) (ms)
    first_click_ms = _Reg(0x15, 4, True) # CLICKED_QUEUE_BACK (ro) (ms)
    led_bright = _Reg(0x19, 1) # LED_BRIGHTNESS (0 - 255)
    led_gran = _Reg(0x1a, 1) # LED_PULSE_GRANULARITY (suggest 1)
    led_cycle_ms = _Reg(0x1b, 2) # LED_PULSE_CYCLE_TIME (ms)
    led_off_ms = _Reg(0x1d, 2) # LED_PULSE_OFF_TIME (ms)
    i2c_addr = _Reg(0x1f, 1) # I2C_ADDRESS

    @property
    def version(self):
#       """Return firmware version number."""
        return (self._fwmaj << 8) | self._fwmin

    @property
    def status(self):
#       """Button status (available, been_clicked, is_pressed)."""
        s = self._bs
        return _BS(
            (s&_BS_EVENT != 0),
            (s&_BS_CLICKED != 0),
            (s&_BS_PRESSED != 0))

    def clear(self):
#       """Reset button status."""
        self._bs = 0

    def _qstat(self, which):
#       """Get the status (empty, full) of the specifed queue."""
        v = getattr(self, which)
        return _QS((v&_QS_EMPTY != 0), (v&_QS_FULL != 0))

    def _qpop(self, which):
#       """Request pop of the specified queue."""
        s = self._qstat(which)
        v = _QS_POP
        if s.empty:
            v |= _QS_EMPTY
        if s.full:
            v |= _QS_FULL
        setattr(self, which, v)

    @property
    def click_queue(self):
#       """Status of the click queue (empty, full).""
        return self._qstat('_clqs')

    def pop_click_queue(self):
#       """Grab the time in ms since first clicked, then pop the click queue."""
        if self.click_queue.empty:
            raise ButtonError('click queue is empty')
        qtm = self.first_click_ms # oldest click
        self._qpop('_clqs')
        return qtm

    @property
    def press_queue(self):
#       """Status of the press queue (empty, full).""
        return self._qstat('_prqs')

    def pop_press_queue(self):
#       """Grab the time in ms since first pressed, then pop the press queue."""
        if self.press_queue.empty:
            raise ButtonError('press queue is empty')
        qtm = self.first_press_ms # oldest press
        self._qpop('_prqs')
        return qtm

    @property
    def interrupts(self):
#       """Return interrupts settings (on_click, on_press)."""
        s = self._int
        return _INT((s&_INT_CL != 0), (s&_INT_PR != 0))
 
    def set_on_click(self, enable=True):
#       """Enable or disable on_click interrupt.
#
#           :param enable: True to enable interrupt (default)
#       """
        if enable:
            self._int |= _INT_CL
        else:
            self._int &= ~_INT_CL & 0xff

    def set_on_press(self, enable=True):
#       """Enable or disable on_press interrupt.
#
#           :param enable: True to enable interrupt (default)
#       """
        if enable:
            self._int |= _INT_PR
        else:
            self._int &= ~_INT_PR & 0xff
