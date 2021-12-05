"""
Module contains function to check strings whether they are empty.

Functions:
    check_empty_strings(*args)
"""
import re


def check_empty_strings(*args):
    """
    Function checks strings whether they are empty
    :param args: strings
    :return: True if all strings are not empty
            else False
    """
    for i in args:
        if re.match(r'^[\s]*$', i):
            return False
    return True
