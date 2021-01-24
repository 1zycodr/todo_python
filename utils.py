# -*- coding: utf-8 -*-

from custom_exceptions import UserInputTextException, UserInputNumException
import re

__all__ = ('get_input_function', )

def raw_input(string):
    result = input(string)
    if len(re.findall('[^A-Z^a-z^\d]', result)):
        raise UserInputTextException
    return result

def num_input(string):
    result = input(string)
    if len(re.findall('[^\d]', result)):
        raise UserInputNumException
    return result
    

def get_input_function():
    try:
        input_function = raw_input
    except NameError:
        input_function = input

    return input_function

def get_input_function_num():
    try:
        input_function = num_input
    except NameError:
        input_function = input

    return input_function