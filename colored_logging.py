#!/usr/bin/env python
# encoding: utf-8

import logging

# holding different stylings for logs
lcolor_profiles = dict()

# Below is the default style.
# feel free to change the formating or use another module to generate the formatting sequences
# (you can of course just enter them manually).

import colorama
from colorama import Fore, Back, Style

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


def level_to_style(level, lvl_to_color):
    """
    :param level: Level of the logging message.
    :param lvl_to_color: A dict defining coloring of each logging message. Format: {level (int): formatting str}.
    :return: Terminal control sequence as string.
    """
    for lvl in sorted(lvl_to_color.keys(), reverse=True):
        if level >= lvl:
            return lvl_to_color[lvl]
    else:
        # no return occurred
        return ""


def return_colored_emit_fct(old_emit_fct, lvl_to_color=lcolor_profiles["default"]):
    """Returns an emit function/method that automatically adds coloring based ont the level of the logging message.
    :param old_emit_fct: Emit function or method (logging.StreamHandler.emit or logging.StreamHandler().emit)
    :param lvl_to_color: A dict defining coloring of each logging message. Format: {level (int): formatting str}.
    :return: emit function/method that automatically adds coloring based on the level of the logging message.
    """
    def colored_emit_fct(*args):
        # Depending on how we use the add_coloring function,
        # the arguments will be different: If we we do
        #    logging.StreamHandler.emit = add_coloring(logging.StreamHandler.emit)
        # the argument types will be (logging.StreamHandler, logging.LogRecord),
        # if we do
        #    sh = logging.StreamHanlder()
        #    sh.emit = add_coloring(sh.emit)
        # we get a single argument of type logging.LogReccord.
        # This function covers both cases.
        for index, arg in enumerate(args):
            if isinstance(arg, logging.LogRecord):
                break
        else:
            # no break occurred / not found ==> abort
            print("Got the following args:")
            for arg in args:
                print("Arg", arg, "of type", type(arg))
            raise(ValueError, "At least one of them snould have been of type logging.LogRecord.")
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

    # unique name (else logging.getLogger will return the same logger every time)
    lname = str(id(color_profile))

    logger = logging.getLogger(lname)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(sh)

    # make sure to test both the standard levels and if nescessary user defined levels.
    standard_levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    test_levels = set(list((color_profile.keys())) + standard_levels)  # (set: make sure to not have duplicates)

    for lvl in sorted(test_levels, reverse=True):
        record = logging.LogRecord(name=lname, level=lvl, pathname=__file__, lineno=86,
                                   msg="Logging message of level {} ({})".format(lvl, logging.getLevelName(lvl)),
                                   args={}, exc_info=None)
        logger.handle(record)


if __name__ == "__main__":
    print("*** TESTING LOG COLOR PROFILES ***")
    for profile_name in lcolor_profiles:
        demo_profile(lcolor_profiles[profile_name], profile_name)