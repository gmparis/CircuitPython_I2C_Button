Introduction
============

.. image:: https://readthedocs.org/projects/circuitpython-i2c_button/badge/?version=latest
    :target: https://circuitpython-i2c_button.readthedocs.io/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://github.com/gmparis/CircuitPython_i2c_button/workflows/Build%20CI/badge.svg
    :target: https://github.com/gmparis/CircuitPython_i2c_button/actions
    :alt: Build Status

CircuitPython I2C Button à la Sparkfun Qwiic Button/Switch/Arcade


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install i2c_button

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. code-block:: python

    import board
    import busio
    from i2c_button import I2C_Button

    i2c = board.I2C()
    button = I2C_Button(i2c)
    print('firmware version is', button.version)

See examples/i2c_button_simpletest.py and other scripts in that folder
for more extensive examples.

Credits
============

This library is based upon the Sparkfun Arduino library and SparkX Switch firmware
authored by Nathan Seidle, Fischer Moseley and Priyanka Makin.

* `Arduino Library <https://github.com/sparkfun/SparkFun_Qwiic_Button_Arduino_Library>`_
* `Switch Firmware <https://github.com/sparkfunX/Qwiic_Switch>`_

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/gmparis/CircuitPython_i2c_button/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
