#!usr/bin/env Python
"""client.py: heavyweight client for multimove
    - Intended for multi-line utility usage
    - All utilities can be called from shell emulator
"""

__author__ = "Efren Haskell"
__email__ = "efrenhask@gmail.com"
__maintainer__ = "Efren Haskell"
__status__ = "Development"
__version__ = "0.0.1"

import itertools
import multimove as mm
import re
from sys import argv
import os

"""
 - get the function
 - get the parameters
 - get the flags
"""


class __Move:

    def __init__(self, command_list: list[str]):
        self.command = command_list
        self.flag_count = 0
        self.flag_map = {
            "-c": False,
            "-sd": False,
        }
        self.params = {
            "des": [],
            "reg": "",
            "src": []
        }
        self.paths = None

    def config_paths(self):
        self.handle_flags()
        src = self.params["src"]
        des = self.params["des"]
        if len(src) != len(des):
            print("Number of source and destination files unmatched")
            return
        self.paths = {src[index].strip(): des[index].strip() for index in range(len(src))}

    def handle_flags(self):
        if self.flag_map["-sd"]:
            self.sd_flag()

    def sd_flag(self):
        if len(self.params['des']) == 0:
            print("A destination is required for use of -sd flag")
            return
        sd: str = self.params['des'][0]
        self.params['des'].clear()
        for src in self.params['src']:
            if "/" in src:
                src_name = src[src.rfind("/"):]
            elif "\\" in src:
                src_name = src[src.rfind("\\"):]
            else:
                src_name = "/" + src
            self.params['des'].append(sd + src_name)

    def set_configuration(self):
        self.__get_flags()
        self.__get_params()

    def __get_flags(self):
        for flag in itertools.takewhile(lambda x: x[0] == '-', self.command):
            if flag not in self.flag_map:
                continue
            self.flag_map[flag] = True
            self.flag_count += 1

    def __get_params(self):
        for index in range(self.flag_count, len(self.command)):
            curr = self.command[index]
            if curr.startswith("src"):
                self.__parse_params("src", curr)
            elif curr.startswith("des"):
                self.__parse_params("des", curr)
            elif curr.startswith("reg"):
                self.__parse_params("reg", curr)

    def __parse_params(self, param_type: str, curr: str):
        self.params[param_type] = curr[4:].strip("\"").split(",")


class __DMove(__Move):
    def __init__(self, command_list: list[str]):
        super().__init__(command_list)

    def call(self):
        self.set_configuration()
        self.config_paths()
        # print(self.paths)
        mm.dict_move(paths=self.paths, cache_moves=self.flag_map["-c"])


class __REMove(__Move):
    def __init__(self, command_list: list[str]):
        super().__init__(command_list)

    def call(self):
        self.set_configuration()
        src_directory = "./" if len(self.params["src"]) == 0 else self.params["src"][0]
        des_directory = "./" if len(self.params["des"]) == 0 else self.params["des"][0]
        mm.re_move(des_directory, src_directory, self.params["reg"][0], cache_moves=self.flag_map["-c"])


def __iterate_args(vals: list[str]):
    if len(vals) == 0:
        return
    function = vals[0]
    if function == "undo":
        return mm.undo_move()
    if function == "prev":
        return mm.print_log()
    fun_constructor = None
    if function == "dm":
        fun_constructor = __DMove(vals[1:])
    elif function == "rem":
        fun_constructor = __REMove(vals[1:])
    else:
        return os.system(" ".join(vals))
    fun_constructor.call()


def __run_heavy():
    while True:
        inp = input(">> ")
        if len(inp) == 0:
            continue
        if inp == "exit":
            exit()
        __iterate_args(re.split(''' +(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', inp))
        # regex to split on whitespace, ignoring quoted sections


def __run_lite():
    if len(args) == 2:
        exit()
    __iterate_args(args[2:])


if __name__ == "__main__":
    args = argv
    if len(args) == 1:
        __run_heavy()
    else:
        __run_lite()
