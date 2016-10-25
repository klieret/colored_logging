#!/usr/bin/env python3

import logging
from colored_logging import ColoredStreamHandler

# Some demo color profile
from demo_profiles import demo_lcolor_profiles

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)

sh = ColoredStreamHandler(demo_lcolor_profiles['default'])
logger.addHandler(sh)

logger.error("Some info message.")