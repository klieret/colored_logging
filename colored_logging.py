#!/usr/bin/env python
# encoding: utf-8

import logging
import colorama
colorama.init()


def level_to_style(level, lcolor=None):
    """
    :param level: Level of the logging message.
    :param lcolor: Supply a dictionary that overrides the default coloring. See code for details.
    :return: Terminal control sequence as string.
    """
    # default level number to level name conversion
    lthresh = {50: "critical",
               40: "error",
               30: "warning",
               20: "info",
               10: "debug"}

    # level to color
    if not lcolor:
        lcolor = {"critical": colorama.Back.BLACK + colorama.Fore.RED + colorama.Style.BRIGHT,
                  "error":    colorama.Back.BLACK + colorama.Fore.WHITE + colorama.Style.BRIGHT,
                  "warning":  colorama.Fore.RED + colorama.Style.BRIGHT,
                  "info":     "",
                  "debug":    colorama.Style.DIM}

    for lvl in sorted(lthresh.keys(), reverse=True):
        if level >= lvl:
            return lcolor[lthresh[lvl]]


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
        args[index].msg = color + args[index].msg + colorama.Style.RESET_ALL
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