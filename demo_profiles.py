#!/usr/bin/env python3
# encoding: utf-8

""" Define a few default profiles. Run this script to preview them."""

import logging
import colorama
from colorama import Fore, Back, Style
from colored_logging import preview_coloring
colorama.init()

# to provide cross-platform terminal colors, this module uses the colorama
# module. See https://pypi.python.org/pypi/colorama (e.g. install via
# sudo pip3 colorama)

# Below are a few default color profiles.
# feel free to change the formating or use another module to generate the
# formatting sequences (or just enter them manually).

demo_lcolor_profiles = {}

demo_lcolor_profiles["default"] = {
    logging.CRITICAL: Back.BLACK + Fore.RED + Style.BRIGHT,
    logging.ERROR:    Back.BLACK + Fore.WHITE + Style.BRIGHT,
    logging.WARNING:  Fore.RED + Style.BRIGHT,
    logging.INFO:     "",
    logging.DEBUG:    Style.DIM,
    0:                Style.RESET_ALL}

demo_lcolor_profiles["simple"] = {
    logging.CRITICAL: Fore.RED + Style.BRIGHT,
    logging.ERROR:    Fore.RED + Style.BRIGHT,
    logging.WARNING:  Fore.MAGENTA + Style.BRIGHT,
    logging.INFO:     Fore.GREEN + Style.BRIGHT,
    logging.DEBUG:    Fore.GREEN,
    0:                Style.RESET_ALL}

demo_lcolor_profiles["dim"] = {1: Style.DIM,
                               0: Style.RESET_ALL}

demo_lcolor_profiles["black"] = {0: Style.RESET_ALL}


if __name__ == "__main__":
    print("*** TESTING COLOR PROFILES ***")
    for profile_name in demo_lcolor_profiles:
        preview_coloring(demo_lcolor_profiles[profile_name], profile_name)
