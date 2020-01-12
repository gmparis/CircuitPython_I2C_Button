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
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_.

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/circuitpython-i2c-button/>`_. To install for current user:

.. code-block:: shell

    pip3 install circuitpython-i2c-button

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install circuitpython-i2c-button

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install circuitpython-i2c-button

Usage Example
=============

.. code-block:: python

    import board
    import busio
    from i2c_button import I2C_Button
    i2c = busio.I2C(board.SCL, board.SDA)
    button = I2C_Button(i2c)
    print('firmware version is', button.version)

See examples/i2c_button_simpletest.py for a more extensive example.

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
