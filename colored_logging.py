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


def level_to_style(level, lvl_to_color):
    """
    :param level: Level of the logging message.
    :param lvl_to_color: Supply a dictionary that overrides the default coloring of the form level (int): formatting str
    :return: Terminal control sequence as string.
    """
    for lvl in sorted(lvl_to_color.keys(), reverse=True):
        if level >= lvl:
            return lvl_to_color[lvl]


def return_colored_emit_fct(old_emit_fct, lvl_to_color=lcolor_profiles["default"]):
    """Returns an emit function/method that automatically adds coloring based ont the level of the logging message.
    :param old_emit_fct: Emit function or method (logging.StreamHandler.emit or logging.StreamHandler().emit)
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
            # no break occurred / not found
            print(args)
            raise(ValueError, "At least one of the arguments has to be of type logging.LogRecord.")
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
    :param color_profile: Level-to-color dictionary (e.g. {10: Style.DIM, logging.ERROR: Fore.RED}
    :param name: Name of the profile (if any). Will print heading, that's all.s
    :return:None
    """
    if name:
        print("*** Testing color profile '{}' ***".format(name))
    lname = "test"
    logger = logging.getLogger(lname)
    logger.setLevel(logging.DEBUG)
    sh = ColoredStreamHandler(lvl_to_color=color_profile)
    logger.addHandler(sh)

    for lvl in sorted(color_profile.keys()):
        record = logging.LogRecord(name=lname, level=lvl, pathname=__file__, lineno=86,
                                   msg="Logging message of level {} ({})".format(lvl, logging.getLevelName(lvl)),
                                   args={}, exc_info=None)
        logger.handle(record)


if __name__ == "__main__":
    for profile_name in lcolor_profiles:
        demo_profile(lcolor_profiles[profile_name], profile_name)