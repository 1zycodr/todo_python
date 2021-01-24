from __future__ import print_function
import sys
import inspect
import json
from custom_exceptions import UserExitException, UserInputNumException, UserInputTextException
from models import BaseItem
from utils import get_input_function, get_input_function_num

class BaseCommand(object):
    @staticmethod
    def label():
        raise NotImplemented()

    def perform(self, objects, *args, **kwargs):
        raise NotImplemented()

    @staticmethod
    def user_input_secure_wrap(func, *args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except UserInputTextException:
                print('Incorrect text.')
            except UserInputNumException:
                print('Incorrect number.')
            except ValueError:
                print('Bad input, try again.')
            except IndexError:
                print('Wrong index, try again.')


class ListCommand(BaseCommand):
    
    @staticmethod
    def label():
        return 'list'

    def perform(self, objects, *args, **kwargs):
        if len(objects) == 0:
            print('There are no items in storage.')
            return

        for index, obj in enumerate(objects):
            # print('{}: {} {}'.format(index, '+' if obj.done is True else '-', str(obj)))
            print('{}: {}'.format(index, str(obj)))


class NewCommand(BaseCommand):
    @staticmethod
    def label():
        return 'new'

    @staticmethod
    def _load_item_classes():
        from models import ToDoItem, ToReadItem , ToBuyItem

        return {
            'ToDoItem': ToDoItem,
            'ToBuyItem': ToBuyItem,
            'ToReadItem': ToReadItem,
        }

    def perform(self, objects, *args, **kwargs):
        classes = self._load_item_classes()

        for index, name in enumerate(classes.keys()):
            print('{}: {}'.format(index, name))

        input_function = get_input_function_num() 
        selection = None
        selected_key = None

        def give_me_num():
            selection = int(input_function('Input number: '))
            selected_key = list(classes.keys())[selection]
            return selected_key

        selected_key = self.user_input_secure_wrap(give_me_num)
        
        selected_class = classes[selected_key]
        print('Selected: {}'.format(selected_class.__name__))
        print()

        new_object = selected_class.construct()

        objects.append(new_object)
        print('Added {}'.format(str(new_object)))
        print()
        return new_object


class DoneCommand(BaseCommand):
    def __init__(self):
        self.flag = True

    @staticmethod
    def label():
        return 'done'
    
    def perform(self, objects, *args, **kwargs):
        if len(objects) == 0:
            print('There are no items in storage.')
            return
        
        for index, name in enumerate(objects):
            print('{}: {}'.format(index, name))
            
        input_function = get_input_function_num()
        selection = None
        selected_item = None

        def give_me_num():
            selection = int(input_function('Input number: '))
            selected_item = objects[selection]
            return selected_item
        
        selected_item = self.user_input_secure_wrap(give_me_num)
        selected_item.done = self.flag

class UndoneCommand(DoneCommand):
    def __init__(self):
        self.flag = False
    @staticmethod
    def label():
        return 'undone'
class ExitCommand(BaseCommand):
    @staticmethod
    def label():
        return 'exit'

    def perform(self, objects, *args, **kwargs):
        raise UserExitException('See you next time!')












