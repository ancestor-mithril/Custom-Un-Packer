from __future__ import print_function

import re
from re import Pattern

from termcolor import colored, cprint
import sys


def error_print(*args, **kwargs):
    """
    same as print but prints to stderr

    :param args:
    :param kwargs:
    :return:
    """
    print(*args, file=sys.stderr, **kwargs)


def color_print(*args, color: str = 'blue', **kwargs):
    """
    same as print but colored

    :param color:
    :param args:
    :param kwargs:
    :return:
    """
    args = [colored(str(x), color) for x in args]
    print(*args, **kwargs)