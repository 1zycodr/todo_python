# -*- coding: utf-8 -*-

from utils import get_input_function, get_input_function_num
from custom_exceptions import *

class Storage(object):  # storage = Storage()
    obj = None
    items = None

    @classmethod
    def __new__(cls, *args):
        if cls.obj is None:
            cls.obj = object.__new__(cls)
            cls.items = []
        return cls.obj
    

class BaseItem(object):
    def __init__(self, heading):
        self.heading = heading
        self.done = False

    def __repr__(self):
        return self.__class__

    def _done_status_repr(self):
        return '+' if self.done is True else '-'

    @classmethod
    def construct(cls):
        raise NotImplemented()


class ToDoItem(BaseItem):
    def __str__(self):
        done_status = self._done_status_repr()
        return '{} ToDo: {}'.format(
            done_status,
            self.heading
        )

    @classmethod
    def construct(cls):
        input_function = get_input_function()
        def get_info(string):
            while True:
                try:
                    heading = input_function(string)
                    break
                except UserInputTextException:
                    print('Error. Enter correct info!')
            return heading

        heading = get_info('Item: ')
        return ToDoItem(heading)

class ToReadItem(BaseItem):
    def __init__(self, heading, link):
        super().__init__(heading)
        self.link = link

    def __str__(self):
        done_status = self._done_status_repr()
        return '{} ToRead: {} ({})'.format(
            done_status,
            self.heading, 
            self.link
        )

    @classmethod
    def construct(cls):
        input_function = get_input_function()

        def get_info(string):
            while True:
                try:
                    heading = input_function(string)
                    break
                except UserInputTextException:
                    print('Error. Enter correct info!')
            return heading

        heading = get_info('Book name: ')
        link = get_info('Book link: ')

        return ToReadItem(heading, link)


class ToBuyItem(BaseItem):
    def __init__(self, heading, price):
        super().__init__(heading)
        self.price = price

    def __str__(self):
        done_status = self._done_status_repr()
        return '{} ToBuy: {} ({})'.format(
            done_status,
            self.heading,
            self.price
        )

    @classmethod
    def construct(cls):
        input_function = get_input_function()
        input_function_num = get_input_function_num()

        
        def get_heading():
            while True:
                try:
                    heading = input_function('Item name: ')
                    break
                except UserInputTextException:
                    print('Error. Enter correct name!')
            return heading

        def get_price():
            while True:
                try:
                    price = input_function_num('Item price: ')
                    break
                except UserInputNumException:
                    print('Error. Enter number!')
            return price

        heading = get_heading()
        price = get_price()

        return ToBuyItem(heading, price)