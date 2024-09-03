#!usr/bin/env python

"""multimove.py: Multi-move operations simplified and automated"""

__author__ = "Efren Haskell"
__email__ = "efrenhask@gmail.com"
__maintainer__ = "Efren Haskell"
__status__ = "Development"
__version__ = "0.0.1"

import os
import re
from shutil import move

# stores past moves if caching is specified
__move_log: list[dict[str, str]] = []


def __move(source: str, destination: str):
    """
    Calls system mv command
    :param source:
    :param destination:
    :return:
    """
    if os.path.exists(source):
        move(source, destination)
    else:
        print(f"{source} is not a valid file path")


def dict_move(paths: dict[str], cache_moves=False):
    """
    Moves all files specified in dictionary parameter
    :param paths:
    :param cache_moves:
    :return:
    """
    if cache_moves:
        __move_log.append(paths)
    for source, destination in paths.items():
        __move(source, destination)


def print_log(index: int = -1):
    length = len(__move_log)
    if length > 0 and index < length:
        for src, dest in __move_log[index].items():
            print(f"{src} -> {dest}")


def re_move(dest_directory: str = "./", parent_directory: str = "./", regex: str = ".*", cache_moves: bool = False):
    """
    Moves all files in a directory that match a regular expression
    Can only be used when all files are to be moved to one destination directory
    :param dest_directory:
    :param parent_directory:
    :param regex:
    :param cache_moves:
    :return:
    """
    if cache_moves:
        __move_log.append({})
    compiled_regex = re.compile(regex)
    path_sep = os.sep
    if not os.path.exists(parent_directory):
        raise FileNotFoundError
    for file in os.scandir(parent_directory):
        file_str = file.name
        if compiled_regex.match(file_str):
            src = path_sep.join((parent_directory, file_str))
            dest = path_sep.join((dest_directory, file_str))
            __move(src, dest)
            if cache_moves:
                __move_log[-1][src] = dest


def undo_move():
    """
    Calls move on move_log items if items are stored in the collection
    :return:
    """
    if len(__move_log) > 0:
        for src, dest in __move_log[-1].items():
            __move(dest, src)
        __move_log.pop(-1)


def verify_move(destination_directory: str = "./", source_directory: str = "./"):
    """
    Prints source and destination files so a user can verify items were moved correctly
    :param source_directory:
    :param destination_directory:
    :return:
    """
    print(f"Source:{source_directory}")
    for file in os.scandir(source_directory):
        print(file.name)
    print(f"____________________________\nDestination:{destination_directory}")
    for file in os.scandir(destination_directory):
        print(file.name)


def verify_re(parent_directory: str = "./", regex: str = ".*"):
    """
    Checks that a regular expression would specify the expected files
    :param parent_directory:
    :param regex:
    :return:
    """
    compiled_regex = re.compile(regex)
    for file in os.scandir(parent_directory):
        file_str = file.name
        if compiled_regex.match(file_str):
            print(file_str)
