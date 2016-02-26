#!/usr/bin/env python
# encoding: utf-8

import logging
import colorama
from colorama import Fore, Back, Style
colorama.init()


def level_to_style(level, lvl_to_color=None):
    """
    :param level: Level of the logging message.
    :param lvl_to_color: Supply a dictionary that overrides the default coloring of the form level (int): formatting str
    :return: Terminal control sequence as string.
    """
    # level to color
    if not lvl_to_color:
        # default
        # either use the keys from $name_to_lvl or just use the level numbers
        lvl_to_color = {logging.CRITICAL: Back.BLACK + Fore.RED + Style.BRIGHT,
                        logging.ERROR:    Back.BLACK + Fore.WHITE + Style.BRIGHT,
                        logging.WARNING:  Fore.RED + Style.BRIGHT,
                        logging.INFO:     "",
                        logging.DEBUG:    Style.DIM}

    for lvl in sorted(lvl_to_color.keys(), reverse=True):
        if level >= lvl:
            return lvl_to_color[lvl]


def return_colored_emit_fct(old_emit_fct):
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
        for index, arg in enumerate(args):
            if isinstance(arg, logging.LogRecord):
                break
        else:
            # no break occurred / not found
            raise(ValueError, "At least one of the arguments has to be of type logging.LogRecord.")
        levelno = args[index].levelno
        color = level_to_style(levelno)
        args[index].msg = color + args[index].msg + Style.RESET_ALL
        return old_emit_fct(*args)
    return colored_emit_fct


class ColoredStreamHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__()

ColoredStreamHandler.emit = return_colored_emit_fct(logging.StreamHandler.emit)


if __name__ == "__main__":
    logger = logging.getLogger("ColoringTest")
    logger.setLevel(logging.DEBUG)
    sh = ColoredStreamHandler()
    logger.addHandler(sh)
    print("Testing logging color settings.")
    print("-"*50)
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical error message.")
    print("-"*50)