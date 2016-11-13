#!/usr/bin/env python3

import logging

# Some demo color profile
from demo_profiles import demo_lcolor_profiles

from colorlog import ColoredStreamHandler


logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)

sh = ColoredStreamHandler(demo_lcolor_profiles['default'])
logger.addHandler(sh)

logger.error("Some error message.")
