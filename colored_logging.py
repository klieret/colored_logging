#!/usr/bin/env python3
# encoding: utf-8

import logging
import colorama
from colorama import Fore, Back, Style
from typing import Dict

# to provide cross-platform terminal colors, this module uses the colorama
# module. See https://pypi.python.org/pypi/colorama (e.g. install via
# sudo pip3 colorama)

# holding different styles for logs
lcolor_profiles = {}

# Below is the default style.
# feel free to change the formating or use another module to generate the formatting sequences
# (you can of course just enter them manually).



colorama.init()

reset_all = Style.RESET_ALL
lcolor_profiles["default"] = {logging.CRITICAL: Back.BLACK + Fore.RED + Style.BRIGHT,
                              logging.ERROR:    Back.BLACK + Fore.WHITE + Style.BRIGHT,
                              logging.WARNING:  Fore.RED + Style.BRIGHT,
                              logging.INFO:     "",
                              logging.DEBUG:    Style.DIM}
lcolor_profiles["simple"] = {logging.CRITICAL: Fore.RED + Style.BRIGHT,
                             logging.ERROR:    Fore.RED + Style.BRIGHT,
                             logging.WARNING:  Fore.YELLOW + Style.BRIGHT,
                             logging.INFO:     Fore.MAGENTA,
                             logging.DEBUG:    Style.DIM}
lcolor_profiles["dim"] = {0: Style.DIM}
lcolor_profiles["black"] = {}


def level_to_style(level: int, lcolor_profile: Dict[int, str]) -> str:
    """
    :param level: Level of the logging message.
    :param lcolor_profile: A dict defining coloring of each logging message.
                           Format: {level (int): formatting str}.
    :return: Terminal control sequence as string.
    """
    for lvl in sorted(lcolor_profile.keys(), reverse=True):
        if level >= lvl:
            return lcolor_profile[lvl]
    else:
        return ""


def return_colored_emit_fct(old_emit_fct,
                            lvl_to_color=lcolor_profiles["default"]):
    """Returns an emit function/method that automatically adds coloring based
    on the logging level.
    :param old_emit_fct: Original Emit function or method:
                         logging.StreamHandler.emit or l
                         ogging.StreamHandler().emit)
    :param lvl_to_color: A dict defining coloring of each logging message.
                         Format: {level (int): formatting str}.
    :return: emit function/method that adds coloring based on the
             logging level"""
    def colored_emit_fct(*args):
        # Depending on how you use this moddle/return_colored_emit_fct,
        # the arguments that will later be given to colored_emit_fct will be
        # different:
        # * Case 1:
        #  logging.StreamHandler.emit = add_coloring(logging.StreamHandler.emit)
        # In this case, colored_emit_fct will be called with the arguments
        # (logging.StreamHandler, logging.LogRecord).
        #
        # * Case 2:
        #    sh = logging.StreamHanlder()
        #    sh.emit = add_coloring(sh.emit)
        # In this case, colored_emit_fct will be called with the argument
        # logging.LogRecord.
        #
        # colored_emit_fct can handle both cases.
        for index, arg in enumerate(args):
            if isinstance(arg, logging.LogRecord):
                break
        else:
            # no 'break' occurred / LogRecord not found ==> abort
            abort_msg = ["Got the following args:"]
            abort_msg.extend(["Arg {} of type {}".format(arg, type(arg))
                              for arg in args])
            abort_msg.append("At least one of them should have been of type "
                             "logging.LogRecord.")
            raise(ValueError, '\n'.join(abort_msg))
        levelno = args[index].levelno
        color = level_to_style(levelno, lvl_to_color)
        args[index].msg = color + args[index].msg + reset_all
        return old_emit_fct(*args)
    return colored_emit_fct


class ColoredStreamHandler(logging.StreamHandler):
    def __init__(self, lvl_to_color=lcolor_profiles["default"], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lvl_to_color = lvl_to_color

    def emit(self, *args, **kwargs):
        return_colored_emit_fct(logging.StreamHandler.emit, self.lvl_to_color)(self, *args, **kwargs)


def demo_profile(color_profile, name=""):
    """Demonstrate a color profile by issuing logging messages on all defined levels.
    :param color_profile: A dict defining coloring of each logging message. Format: {level (int): formatting str}.
    :param name: Name of the profile. If supplied, logging messages will be indented and there will be a heading.
    :return:None
    """
    if name:
        print("'{}' profile".format(name))
        indent = 5
    else:
        indent = 0

    formatter = logging.Formatter(" "*indent + '%(asctime)s - %(levelname)s - %(message)s')

    sh = ColoredStreamHandler(lvl_to_color=color_profile)
    sh.setFormatter(formatter)

    # unique name (else logging.getLogger will return the same logger every
    # time)
    lname = str(id(color_profile))

    logger = logging.getLogger(lname)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(sh)

    # make sure to test both the standard levels and if nescessary user defined
    # levels.
    standard_levels = [logging.DEBUG, logging.INFO, logging.WARNING,
                       logging.ERROR, logging.CRITICAL]
    # make sure to not have duplicates
    all_levels = set(list((color_profile.keys())) + standard_levels)

    for lvl in sorted(all_levels, reverse=True):
        msg = "Logging message of level {} ({})".format(lvl, logging.getLevelName(lvl))
        record = logging.LogRecord(name=lname,
                                   level=lvl,
                                   pathname=__file__,
                                   lineno=86,
                                   msg=msg,
                                   args={},
                                   exc_info=None)
        logger.handle(record)


if __name__ == "__main__":
    print("*** TESTING COLOR PROFILES ***")
    for profile_name in lcolor_profiles:
        demo_profile(lcolor_profiles[profile_name], profile_name)