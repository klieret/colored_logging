# Color for the python3 logging module

For use together with the python3 logging module: Allows to automatically color logging messages based on their level.

![colored logging](scrot.png)

## Usage

Minimal example, using one of the predefined color schemes from ```demo_profiles.py```:

```pyhon
import logging
from colored_logging import ColoredStreamHandler

# Some demo color profile
from demo_profiles import demo_lcolor_profiles

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)

sh = ColoredStreamHandler(demo_lcolor_profiles['default'])
logger.addHandler(sh)

logger.error("Some info message.")
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
    0:                Style.RESET_ALL
}

sh = ColoredStreamHandler(my_profile)

(...)
```

** Note: Always define a reset sequence that resets the color/formatting to the default value at level 0! **