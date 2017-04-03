# Color for the python3 logging module

[![Build Status](https://travis-ci.org/klieret/python-colorlog.svg?branch=master)](https://travis-ci.org/klieret/python-colorlog)

For use together with the python3 logging module: Allows to automatically color logging messages based on their level.

![screenshot](https://cloud.githubusercontent.com/assets/13602468/20245019/fa888894-a996-11e6-8ad4-d3862d515d08.png)

## Installation

As this project is still in development, you have to clone the repository first and then install it with ```pip```:

```sh
git clone https://github.com/klieret/python-colorlog
cd python-colorlog
pip3 install .
```

## Usage

Minimal example, using one of the predefined color schemes from ```demo_profiles.py```:

```python
import logging
from colored_logging import ColoredStreamHandler

# Some demo color profile
from demo_profiles import demo_lcolor_profiles

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)

sh = ColoredStreamHandler(demo_lcolor_profiles['default'])
logger.addHandler(sh)

logger.error("Some error message.")
```

Color profiles are ```int:str``` dictionaries that map level numbers to formatting strings. To do this platform independent, it is recommended to use some module like ```colorama```:

```python
import logging
from colored_logging import ColoredStreamHandler

import colorama
from colorama import Fore, Back, Style
colorama.init()

my_profile = {
    logging.CRITICAL: Fore.RED + Style.BRIGHT,
    logging.ERROR:    Fore.RED + Style.BRIGHT,
    logging.WARNING:  Fore.MAGENTA + Style.BRIGHT,
    logging.INFO:     Fore.GREEN + Style.BRIGHT,
    logging.DEBUG:    Fore.GREEN,
    -1:               Style.RESET_ALL
}

sh = ColoredStreamHandler(my_profile)

(...)
```

**Note: Always define a reset sequence (to the key -1) that resets the color/formatting to the default value**

## License

The contents of this repository are licensed under the *GNU Lesser General Public License v3.0*. 
