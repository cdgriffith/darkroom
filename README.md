# darkroom

This is my code for a darkroom timer using:

* RaspberryPi
* IoT Relay (power switch)
* 8x8 x4 LED Matrix
* USB Numpad

## Installing

Please use the [guide from CodeCalamity](https://codecalamity.com/build-your-own-pi-powered-enlarger-timer/).

In short:

* [Enable SPI](https://luma-led-matrix.readthedocs.io/en/latest/install.html#max7219-devices)
* Add user to proper groups `sudo usermod -a -G spi,gpio pi`
* Install pre-reqs `sudo apt install -y build-essential python3-dev libfreetype6-dev libjpeg-dev libopenjp2-7 libtiff5`
* Create a virtual env `python3 -m venv`
* Activate env `source venv/bin/activate`
* Update pip `python -m pip install --upgrade --ignore-installed pip setuptools`
* Install requirements `pip install -r requirements`
* Run the program `python -m darkroom`


## Key controls

```
*      Start key capture (to input time via number keys)
+      Add a tenth of a second
-      Remove a tenth of a second
/      "Focus" - Turn the enlarger on
ENTER  "Print" - Enlarger on, timer countdown, auto enlarger off
```

## License

This is MIT Licensed, view the LICENSE file for details.

This is using the Free for personal use Scoreboard font available at https://www.ffonts.net/Score-Board.font
