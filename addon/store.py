# -*- coding:utf-8 -*-

from .base import *
from utils import *

import sys


i18n = {
    "zh_CN": {
        "description": "持久化存储键值对数据",
        "write_help": "存储键值数据",
        "read_help": "读取键值数据",

    },
    "en_US": {
        "description": "store key-value in disk",
        "write_help": "write key-value",
        "read_help": "read key-value",
    },
}


class Store(Addon):
    def __init__(self):
        debug(ctx)
        self.lang = I18n(i18n)

    def name(self):
        return ["s", "store"]

    def description(self):
        return self.lang.get("description")

    def run(self, params):
        if ctx.help:
            print(
                "o store {write|read} {key} [value]\n    " +
                self.description()
            )
            exit(0)

        if len(params) < 1:
            print("error: missing command, want write or read")
            exit(1)
        cmd = params[0]

        if len(params) < 2:
            print("error: missing key")
            exit(1)
        key = params[1]

        if cmd in ["write", "w"]:
            if len(params) < 3:
                print("error: missing value")
                exit(1)
            value = params[2]
            kvStore(key, value)
        elif cmd in ["read", "r"]:
            print(kvLoad(key, ""))
        else:
            print("Unknown command " + cmd)


addons.append(Store)
