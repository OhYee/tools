# -*- coding:utf-8 -*-

from .base import *
from utils import *

import json
import re
import os
import time

_WATCH_REFRESH_TIME = 1
_WATCH_COUNT = 10
_WATCH_FLOAT = 3
i18n = {
    "zh_CN": {
        "description": "监控数字变动",
        "time_help": "刷新周期，默认 %d 秒" % _WATCH_REFRESH_TIME,
        "number_help": "保存的数字个数，默认 %d" % _WATCH_COUNT,
        "history_help": "不显示保存的数字记录",
        "float_help": "保留的小数位数，默认 %d" % _WATCH_FLOAT,
    },
    "en_US": {
        "description": "watch numbers",
        "time_help": "refresh time period，defaykt %d second" % _WATCH_REFRESH_TIME,
        "number_help": "the number kept in history，default %d" % _WATCH_COUNT,
        "history_help": "do not show kept history",
        "float_help": "float number precision，default %d" % _WATCH_FLOAT,
    },
}


class Watch(Addon):
    def __init__(self):
        debug("Init JSON", ctx)
        self.lang = I18n(i18n)

    def name(self):
        return ["w", "watch"]

    def description(self):
        return self.lang.get("description")

    def run(self, params):
        flags = Flags("o watch [command 1] [command 2...] [options]", params)
        flags.addOption(
            ["-t", "--time"],
            self.lang.get("time_help"),
            False,
        )
        flags.addOption(
            ["-n", "--number"],
            self.lang.get("number_help"),
            True,
        )
        flags.addOption(
            ["--no-history"],
            self.lang.get("history_help"),
            False,
        )
        flags.addOption(
            ["-f", "--float"],
            self.lang.get("float_help"),
            True,
        )
        debug(flags.parse())

        if ctx.help:
            flags.showHelp()

        sleep_time = flags.int("-t", _WATCH_REFRESH_TIME)
        number = flags.int("-n", _WATCH_COUNT)
        no_history = flags.bool("--no-history")
        float_fmt = "%%.%df" % flags.int("-f", _WATCH_FLOAT)
        commands = flags.restArgs()
        debug("commands", commands)

        l = len(commands)
        slice = [[] for _ in range(l)]

        while True:
            for idx, cmd in enumerate(commands):
                try:
                    p = os.popen(cmd)
                    value = float(p.read())
                except Exception as e:
                    stderrLine(e)
                    value = 0
                slice[idx].append(value)
                if len(slice[idx]) > number:
                    slice[idx] = slice[idx][-number:]

            print("\033[H\033[2J")
            for idx in range(l):
                print(commands[idx])
                if not no_history:
                    print(slice[idx])
                print(
                    "Min:", float_fmt % min(slice[idx]),
                    "Max:", float_fmt % max(slice[idx]),
                    "Sum:", float_fmt % sum(slice[idx]),
                    "Avg:", "NaN" if len(slice[idx]) == 0 else float_fmt % (
                        sum(slice[idx]) / len(slice[idx])
                    )
                )
                print()

            time.sleep(sleep_time)

    def parse(self, repl, text):
        return text if re.match(repl, text) != None else None

    def get(self, params):
        pass


addons.append(Watch)
