#!/usr/bin/env python3
# encoding: utf-8

""" Module to color logging messages of the logging module based on the
logging level. """

import logging
from typing import Dict


def level_to_style(level: int, lcolor_profile: Dict[int, str]) -> str:
    """
    :param level: Level of the logging message.
    :param lcolor_profile: A dict defining the coloring of each logging
                           message. Format: {level (int): formatting str}.
    :return: Terminal control sequence as string.
    """
    for lvl in sorted(lcolor_profile.keys(), reverse=True):
        if level >= lvl:
            return lcolor_profile[lvl]
    else:
        return ""


def return_colored_emit_fct(old_emit_fct,
                            color_dict=Dict[int, str]):
    """Returns an emit function/method that automatically adds coloring based
    on the logging level.
    :param old_emit_fct: Original Emit function or method:
                         logging.StreamHandler.emit or
                         logging.StreamHandler().emit)
    :param color_dict: A dict defining coloring of each logging message.
                       Format: {level (int): formatting str}.
    :return: emit function/method that adds coloring based on the
             logging level"""
    def colored_emit_fct(*args):
        # Depending on how you use this moddle/return_colored_emit_fct,
        # the arguments that will later be given to colored_emit_fct will be
        # different:
        #
        # * Case 1: (Global replacement)
        #    logging.StreamHandler.emit =
        #                return_colored_emit_fct(logging.StreamHandler.emit)
        # In this case, colored_emit_fct will be called with the arguments
        # (logging.StreamHandler, logging.LogRecord).
        #
        # * Case 2:
        #    sh = logging.StreamHandler()
        #    sh.emit = return_colored_emit_fct(sh.emit)
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
        color = level_to_style(levelno, color_dict)
        args[index].msg = color + args[index].msg + color_dict[0]
        return old_emit_fct(*args)
    return colored_emit_fct


class ColoredStreamHandler(logging.StreamHandler):
    """Use instead of logging.StreamHandler to color the logging messages."""
    def __init__(self, color_dict: Dict[int, str], *args,
                 **kwargs):
        """
        :param color_dict: A dict defining coloring of each logging message.
                           Format: {level (int): formatting str}.
        """
        super().__init__(*args, **kwargs)
        self.emit_fct = return_colored_emit_fct(logging.StreamHandler.emit,
                                                color_dict)

    def emit(self, *args, **kwargs):
        self.emit_fct(self, *args, **kwargs)


def preview_coloring(color_dict, name=""):
    """Preview a color profile by issuing logging messages on all defined
    levels.
    :param color_dict: A dict defining coloring of each logging message.
                          Format: {level (int): formatting str}.
    :param name: Name of the profile. If supplied, logging messages will be
                 indented and there will be a heading.
    :return:None
    """
    if name:
        print("'{}' profile".format(name))
        indent = 5*" "
    else:
        indent = ""

    formatter = logging.Formatter(indent + '%(asctime)s - %(levelname)s -'
                                           ' %(message)s')

    sh = ColoredStreamHandler(color_dict=color_dict)
    sh.setFormatter(formatter)

    # unique name (else logging.getLogger will return the same logger every
    # time)
    lname = str(id(color_dict))

    logger = logging.getLogger(lname)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(sh)

    # make sure to test both the standard levels and user defined levels.
    standard_levels = [logging.DEBUG, logging.INFO, logging.WARNING,
                       logging.ERROR, logging.CRITICAL]
    # make sure to not have duplicates
    all_levels = set(list((color_dict.keys())) + standard_levels)

    for lvl in sorted(all_levels, reverse=True):
        msg = "Logging message of level {}".format(lvl)
        record = logging.LogRecord(name=lname,
                                   level=lvl,
                                   pathname=__file__,
                                   lineno=86,
                                   msg=msg,
                                   args={},
                                   exc_info=None)
        logger.handle(record)
