# SPDX-FileCopyrightText: Copyright (c) 2020,2021 Greg Paris
#
# SPDX-License-Identifier: MIT

# This library based upon Sparkfun's Arduino library and firmware sources:
# github.com/sparkfun/SparkFun_Qwiic_Button_Arduino_Library/blob/master/src
# github.com/sparkfunX/Qwiic_Switch/blob/master/Firmware/Qwiic_Button
"""
`i2c_button`
================================================================================

CircuitPython I2C Button à la Sparkfun Qwiic Button/Switch/Arcade


* Author(s): Greg Paris

Implementation Notes
--------------------

**Hardware:**

* `Sparkfun Qwiic Button-Red <https://www.sparkfun.com/products/15584>`_
* `Sparkfun Qwiic Button-Blue <https://www.sparkfun.com/products/15585>`_
* `Sparkfun Qwiic Switch <https://www.sparkfun.com/products/15586>`_
* `Sparkfun Qwiic Arcade-Red <https://www.sparkfun.com/products/15591>`_
* `Sparkfun Qwiic Arcade-Blue <https://www.sparkfun.com/products/15592>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

* Adafruit's Bus Device library:
  https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

# imports
from collections import namedtuple
from adafruit_bus_device.i2c_device import I2CDevice

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/gmparis/CircuitPython_i2c_button.git"

_ENDIAN = "little"
_DEF_ADDR = 0x6F
_DEV_ID = 0x5D

# Button status flags and tuple
_BS_EVENT = 0x1  # clear after use
_BS_CLICKED = 0x2  # clear after use
_BS_PRESSED = 0x4  # user immutable
_BS = namedtuple("_BS", ("available", "been_clicked", "is_pressed"))

# Interrupt status flags
# _INT_CL = 0x1  # enable an interrupt on button click
# _INT_PR = 0x2  # enable an interrupt on button press
# _INT = namedtuple("_INT", ("on_click", "on_press"))

# Queue status flags and tuple
# _QS_POP = 0x1  # set to pop from queue
# _QS_EMPTY = 0x2  # user immutable
# _QS_FULL = 0x4  # user immutable
# _QS = namedtuple("_QS", ("empty", "full"))

# Commented out due to low utility.
# def _to_qs(status):
#    """Queue status integer to **_QS** tuple."""
#    return _QS((status & _QS_EMPTY != 0), (status & _QS_FULL != 0))


class ButtonError(Exception):
    """Button-related error conditions."""


def _read_register(button, register, n_bytes=1):
    """Write the register number, read back the value."""
    regid = register.to_bytes(1, _ENDIAN)
    buf = bytearray(n_bytes)
    with button.device as dev:
        dev.write_then_readinto(regid, buf)
    return int.from_bytes(buf, _ENDIAN)


def _write_register(button, register, value, n_bytes=1):
    """Write the register number, write the value."""
    buf = bytearray(1 + n_bytes)
    buf[0] = register
    buf[1:] = value.to_bytes(n_bytes, _ENDIAN)
    with button.device as dev:
        dev.write(buf)


# Button Register Descriptor class
class _Reg:
    def __init__(self, addr, width, readonly=False):
        self.addr = addr
        self.width = width
        self.readonly = readonly

    def __get__(self, button, objtype):
        return _read_register(button, self.addr, self.width)

    def __set__(self, button, value):
        if self.readonly:
            raise AttributeError("write to read-only register " + hex(self.addr))
        _write_register(button, self.addr, value, self.width)


# NOTE: This class is sortable and hashable to make it easier
# to organize buttons when one has more than a few.
# If you don't need this functionality, you can comment out the
# lines as noted below and save some memory.
class I2C_Button:
    # pylint: disable=line-too-long
    """I2C-connected button, à la Sparkfun Qwiic Button/Switch/Arcade

    :param i2c_obj: initialized I2C object
    :param i2c_addr: I2C address of the button
    :param dev_id: Device ID of the button
    :param name: a name for the button
    :raises ButtonError: if device I2C address does match the specified device ID

    Besides being connected via I2C, which can provide some advantages when wiring up a project,
    the I2C Button's chief advantage is that it has its own processor, which monitors the
    state of the physical button. It does debouncing. It keeps track of time since the last
    click event and the last press event. It reports whether a button has been pressed or
    has been clicked since its state was last cleared. It can even manage operation of a
    single (user-supplied) LED. That's a lot of processing that the calling program does not
    have to do.

    It should have functionality associated with keeping a queue of events. Unfortunately,
    at the time of writing this, the only firmware available doesn't quite hit the mark when
    it comes to queue management. It is not possible to clear the queues, nor does popping
    an entry off a queue have an effect on its length. Previous versions of this library
    included methods for interacting with the queues, but since they don't work, they waste
    space and potentially waste the time of someone trying to use them. Those methods have
    been commented out in this version of this library.
    """

    def __init__(self, i2c_obj, i2c_addr=_DEF_ADDR, dev_id=_DEV_ID, name="button"):
        self.i2c = i2c_obj
        self.device = I2CDevice(i2c_obj, i2c_addr)
        if self.dev_id != dev_id:
            raise ButtonError(
                f"not button {self.dev_id:02x} at i2c addr {i2c_addr:02x}"
            )
        self._name = name
        self._key = (name, i2c_addr)  # comment out for no sorting/hashing

    # Commment out next four methods if you don't need to compare buttons,
    # for example, by sorting them.
    def __eq__(self, other):
        # pylint: disable=protected-access
        return self._key == other._key

    def __gt__(self, other):
        # pylint: disable=protected-access
        return self._key > other._key

    def __lt__(self, other):
        # pylint: disable=protected-access
        return self._key < other._key

    # Commment out next method if you don't need to hash buttons,
    # for example, by putting them in a set().
    def __hash__(self):
        return hash(self._key)

    # Comment out next if you need a bit more memory.
    def __repr__(self):
        return "%s(%s, i2c_addr=%s, dev_id=%s, name=%s)" % (
            self.__class__.__name__,
            repr(self.i2c),
            hex(self.i2c_addr),
            hex(self.dev_id),
            repr(self.name),
        )

    _fwmin = _Reg(0x01, 1, True)  # FIRMWARE_MINOR (ro)
    _fwmaj = _Reg(0x02, 1, True)  # FIRMWARE_MAJOR (ro)
    _bs = _Reg(0x03, 1)  # BUTTON_STATUS (see _BS flags above)

    # Next three commented out due to low utility.
    #   _int = _Reg(0x04, 1)  # INTERRUPT_CONFIG (see _INT flags above)
    #   _prqs = _Reg(0x07, 1)  # PRESSED_QUEUE_STATUS (see _QS flags above)
    #   _clqs = _Reg(0x10, 1)  # CLICKED_QUEUE_STATUS (see _QS flags above)

    #: Device ID. (1 byte; read-only)
    dev_id = _Reg(0x00, 1, True)

    #: Button debounce time in milliseconds. (4 bytes; read-write)
    debounce_ms = _Reg(0x05, 2)

    #: Time since most recent press in queue in milliseconds. (4 bytes; read-only)
    last_press_ms = _Reg(0x08, 4, True)

    #: Time since oldest press in queue in milliseconds. (4 bytes; read-only)
    #:
    #: Note that with firmware version 1.1, there is no way to clear the
    #: queue, so this value is less useful than it might first seem.
    first_press_ms = _Reg(0x0C, 4, True)

    #: Time since most recent click in queue in milliseconds. (4 bytes; read-only)
    last_click_ms = _Reg(0x11, 4, True)

    #: Time since oldest click in queue in milliseconds. (4 bytes; read-only)
    #:
    #: Note that with firmware version 1.1, there is no way to clear the
    #: queue, so this value is less useful than it might first seem.
    first_click_ms = _Reg(0x15, 4, True)

    #: LED brightness, 0 - 255. (1 byte; read-write)
    led_bright = _Reg(0x19, 1)

    #: LED granularity. A value of 1 is commonly useful. (1 byte; read-write)
    led_gran = _Reg(0x1A, 1)

    #: LED pulse cycle time in milliseconds. (4 bytes; read-write)
    led_cycle_ms = _Reg(0x1B, 2)

    #: LED pulse off time in milliseconds. (4 bytes; read-write)
    led_off_ms = _Reg(0x1D, 2)

    #: Button I2C address. (1 byte; read-write)
    #:
    #: If you set this property, you are changing the I2C address of the button. That change
    #: will persist through power-off. When you make such a change, the :class:`I2C_Button`
    #: instance will become invalid. Probably best to just make any such changes in a separate
    #: program. One of the examples shows this.
    i2c_addr = _Reg(0x1F, 1)

    @property
    def name(self):
        """Button name."""
        return self._name

    #   @property
    #   def version(self):
    #       """Firmware version number. (2 bytes; read-only)"""
    #       return (self._fwmaj << 8) | self._fwmin  # same way as Arduino library but kooky

    @property
    def version(self):
        """Firmware version string (read-only)"""
        return f"{self._fwmaj:d}.{self._fwmin:d}"

    @property
    def status(self):
        """Button status. (**available**, **been_clicked**, **is_pressed** tuple; read-only)"""
        intval = self._bs
        return _BS(
            (intval & _BS_EVENT != 0),
            (intval & _BS_CLICKED != 0),
            (intval & _BS_PRESSED != 0),
        )

    def clear(self):
        """Reset button status."""
        self._bs = 0


# Commented out due to low utility.
#   @property
#   def click_queue(self):
#       """Click queue status. (**empty**, **full** tuple; read-only)
#
#       The utility of this method is low if firmware version is 1.1.
#       This is because the queue is not cleared by **clear()**,
#       nor are entries removed with **pop_click_queue()**."""
#       return _to_qs(self._clqs)

# Commented out until new firmware fixes this issue.
#   def pop_click_queue(self):
#       """Get time since first click, pop click queue, return time.
#
#       Popping the click queue does not work with firmware version 1.1,
#       so this method rasies an exception in that case.
#
#       :raises ButtonError: if queue is empty
#       :raises RuntimeError: if firmware version is 1.1
#       """
#       if self.version == "1.1":
#           raise RuntimeError("unsupported by firmware version")
#       if self.click_queue.empty:
#           raise ButtonError("click queue is empty")
#       qtm = self.first_click_ms  # oldest click
#       self._clqs |= _QS_POP
#       return qtm

# Commented out due to low utility.
#   @property
#   def press_queue(self):
#       """Press queue status. (**empty**, **full** tuple; read-only)
#
#       The utility of this method is low if firmware version is 1.1.
#       This is because the queue is not cleared by **clear()**,
#       nor are entries removed with **pop_press_queue()**."""
#       return _to_qs(self._prqs)

# Commented out until new firmware fixes this issue.
#   def pop_press_queue(self):
#       """Get time since first press, pop press queue, return time.
#
#       Popping the press queue does not work with firmware version 1.1,
#       so this method rasies an exception in that case.
#
#       :raises ButtonError: if queue is empty
#       :raises RuntimeError: if firmware version is 1.1
#       """
#       if self.version == "1.1":
#           raise RuntimeError("unsupported by firmware version")
#       if self.press_queue.empty:
#           raise ButtonError("press queue is empty")
#       qtm = self.first_press_ms  # oldest press
#       self._prqs |= _QS_POP
#       return qtm

# Commented-out due to low utility.
#   @property
#   def interrupts(self):
#       """Interrupts settings. (**on_click**, **on_press** tuple; read-only)
#
#       CircuitPython does not use these interrupts.
#       """
#       intval = self._int
#       return _INT((intval & _INT_CL != 0), (intval & _INT_PR != 0))

# Commented-out due to low utility.
#   def set_on_click(self, enable=True):
#       """Enable or disable **on_click** interrupt.
#
#       :param enable: True to enable interrupt (default)
#
#       This interrupt is not used by CircuitPython.
#       """
#       if enable:
#           self._int |= _INT_CL
#       else:
#           self._int &= ~_INT_CL & 0xFF

# Commented-out due to low utility.
#   def set_on_press(self, enable=True):
#       """Enable or disable **on_press** interrupt.
#
#       :param enable: True to enable interrupt (default)
#
#       This interrupt is not used by CircuitPython.
#       """
#       if enable:
#           self._int |= _INT_PR
#       else:
#           self._int &= ~_INT_PR & 0xFF
