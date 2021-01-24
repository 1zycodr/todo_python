# -*- coding: utf-8 -*-

"""
Main file. Contains program execution logic.
"""

from __future__ import print_function

import inspect
import sys
import json
from commands import (
    ListCommand,
    NewCommand,
    ExitCommand,
    DoneCommand,
    UndoneCommand,
    UserExitException,
)
from models import *
from utils import get_input_function

ITEMS = []

def get_data_from_json():
    with open('data.json') as f:
        data = json.load(f)
    return data

def fill_storage():
    storage = Storage()
    data = get_data_from_json()
    
    
    for obj in data:
        print(obj)
        obj_class = obj['class']
        obj_heading = obj['heading']
        obj_done = obj['done']

        if obj_class == 'ToDoItem':
            item = ToDoItem(obj_heading)
            item.done = obj_done
            storage.items.append(item)
        elif obj_class == 'ToBuyItem':
            obj_price = obj['price']
            item = ToBuyItem(obj_heading, obj_price)
            item.done = obj_done
            storage.items.append(item)
        else:
            obj_link = obj['link']
            item = ToReadItem(obj_heading, obj_link)
            item.done = obj_done
            storage.items.append(item)

def fill_json():
    storage = Storage()
    data = []

    for i in storage.items:
        obj = {
            "class"   : i.__class__.__name__, 
            "heading" : i.heading, 
            "done"    : i.done
        }

        if obj['class'] == 'ToBuyItem':
            obj["price"] = i.price

        if obj['class'] == 'ToReadItem':
            obj["link"] = i.link

        data.append(obj)
    
    with open('data.json', 'w') as f:
        f.write(json.dumps(data))

def get_routes():
    """
    This function contains the dictionary of possible commands.
    :return: `dict` of possible commands, with the format: `name -> class`
    """

    return {
        ListCommand.label(): ListCommand,
        NewCommand.label(): NewCommand,
        DoneCommand.label(): DoneCommand,
        UndoneCommand.label(): UndoneCommand,
        ExitCommand.label(): ExitCommand,
    }


def perform_command(command):
    """
    Performs the command by name.
    Stores the result in `Storage()`.
    :param command: command name, selected by user.
    """

    command = command.lower()
    routes = get_routes()

    try:
        command_class = routes[command]
        command_inst = command_class()

        storage = Storage()
        command_inst.perform(storage.items)
    except KeyError:
        print('Bad command, try again.')
    except UserExitException as ex:
        print(ex)
        raise


def parse_user_input():
    """
    Gets the user input.
    :return: `str` with the user input.
    """

    input_function = input

    message = 'Input your command: (%s): ' % '|'.join(
        {
            ListCommand.label(): ListCommand,
            NewCommand.label(): NewCommand,
            DoneCommand.label(): DoneCommand,
            UndoneCommand.label(): UndoneCommand,
            ExitCommand.label(): ExitCommand,
        }.keys()
    )
    return input_function(message)


def main():
    """
    Main method, works infinitelly until user runs `exit` command.
    Or hits `Ctrl+C` in the console.
    """
    fill_storage()

    while True:
        try:
            command = parse_user_input()
            perform_command(command)
            if command == 'new' or command == 'done' or command == 'undone':
                print('hoerhg')
                fill_json()
        except UserExitException:
            break
        except Exception as e:
            print('You have done something wrong!', e)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        
        print()
        print('Shutting down, bye!')
