#!/usr/bin/env python
# encoding: utf-8

import logging
import colorama
colorama.init()


def convertable_to_int(inpt):
    """
    :param inpt: Anything.
    :return:Int if ``inpt`` can be interpreted as such.
    """
    try:
        int(inpt)
    except ValueError:
        return False
    else:
        return True


def level_to_style(level, misc_to_color=None, name_to_lvl=None):
    """
    :param level: Level of the logging message.
    :param misc_to_color: Supply a dictionary that overrides the default coloring. Keys should either be the level
    numbers, or the strings "critical", "error", "warning", "info" and "debug".
    :return: Terminal control sequence as string.
    """
    # default level number to level name conversion
    if not name_to_lvl:
        name_to_lvl = {"critical": 50,
                       "error": 40,
                       "warning": 30,
                       "info": 20,
                       "debug": 10, }

    # level to color
    if not misc_to_color:
        # default
        # either use the keys from $name_to_lvl or just use the level numbers
        misc_to_color = {"critical": colorama.Back.BLACK + colorama.Fore.RED + colorama.Style.BRIGHT,
                         "error":    colorama.Back.BLACK + colorama.Fore.WHITE + colorama.Style.BRIGHT,
                         "warning":  colorama.Fore.RED + colorama.Style.BRIGHT,
                         "info":     "",
                         "debug":    colorama.Style.DIM}

    lvl_to_color = {}
    for key in misc_to_color:
        if convertable_to_int(key):
            lvl_to_color[int(key)] = misc_to_color[key]
        elif key in name_to_lvl:
            lvl_to_color[name_to_lvl[key]] = misc_to_color[key]
        else:
            raise ValueError

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