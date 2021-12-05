# -*- coding:utf-8 -*-

from .base import *
from utils import *

import sys
import re

i18n = {
    "zh_CN": {
        "description": "高亮日志输出(ERROR 等字符)",
        "regex_help": "高亮正则表达式 regexp[:color][:font style])",
        "number_help": "只显示前 N 行",
        "tail_help": "只显示最后 N 行",
        "follow_help": "保持从文件读入",
        "color_help": "支持的颜色",
        "style_help": "支持的样式",
    },
    "en_US": {
        "description": "highlight output",
        "regex_help": "regex pattern for highlight. regexp[:color][:font style])",
        "number_help": "only show top N lines",
        "tail_help": "only show last N lines",
        "follow_help": "keep read from file",
        "color_help": "color options",
        "style_help": "style options",
    },
}


class Colorful(Addon):
    def __init__(self):
        debug("Init Colorful", ctx)
        self.lang = I18n(i18n)

    def name(self):
        return ["c", "colorful"]

    def description(self):
        return self.lang.get("description")

    def init(self):
        self.colors = {
            "": "",
            "black": "\033[30m",
            "r": "\033[31m",
            "red": "\033[31m",
            "g": "\033[32m",
            "green": "\033[32m",
            "y": "\033[33m",
            "yellow": "\033[33m",
            "b": "\033[34m",
            "blue": "\033[34m",
            "m": "\033[35m",
            "magenta": "\033[35m",
            "c": "\033[36m",
            "cyan": "\033[36m",
            "w": "\033[37m",
            "white": "\033[37m",
        }
        self.colorsRegexp = "^(?:%s){0,1}$" % "|".join(
            ["(?:%s)" % k for k in self.colors.keys() if k != ""]
        )
        debug(self.colorsRegexp)
        self.styles = {
            "": "",
            "b": "\033[1m",
            "bold": "\033[1m",
            "w": "\033[2m",
            "weak": "\033[2m",
            "i": "\033[3m",
            "italics": "\033[3m",
            "u": "\033[4m",
            "underline": "\033[4m",
            "blink": "\033[5m",
            "r": "\033[7m",
            "reverse": "\033[7m",
            "h": "\033[8m",
            "hidden": "\033[8m",
            "d": "\033[9m",
            "delete": "\033[9m",
        }
        self.stylesRegexp = "^(?:%s){0,1}$" % "|".join(
            ["(?:%s)" % k for k in self.styles.keys() if k != ""]
        )
        debug(self.stylesRegexp)

    def run(self, params):
        flags = Flags("o builtin [command] [options]", params)
        flags.addFlag(
            ["-r", "--regex"],
            self.lang.get("regex_help"),
            True,
        )
        flags.addFlag(
            ["-n", "--number"],
            self.lang.get("number_help"),
            True,
        )
        flags.addFlag(
            ["-t", "--tail"],
            self.lang.get("tail_help"),
            True,
        )
        flags.addFlag(
            ["-f", "--follow"],
            self.lang.get("follow_help"),
        )

        debug(flags.parse())

        self.init()

        if ctx.help:
            # flags.showHelp()
            print("\n".join(
                [
                    self.description(),
                    "",
                    "%s: %s" % (
                        self.lang.get("color_help"),
                        "|".join(self.colors.keys()),
                    ),
                    "%s: %s" % (
                        self.lang.get("style_help"),
                        "|".join(self.styles.keys()),
                    ),
                ]
            ))
            exit(0)

        regex = flags.list("-r")
        replaceFunc = []
        for r in regex:
            reg = ""
            color = ""
            style = ""

            if r.endswith("::"):
                reg = r[: -2]
            else:
                lst = r.split(":")
                if len(lst) > 1:
                    color = self.parse(self.colorsRegexp, lst[-2])
                    style = self.parse(self.stylesRegexp, lst[-1])
                    if color != None and style != None:
                        lst = lst[: -2]
                    else:
                        color = self.parse(self.colorsRegexp, lst[-1])
                        style = ""
                        if color != None:
                            lst = lst[: -1]
                    reg = ":".join(lst)

            debug(r, "=>", "(", reg, "|", color, "|", style, ")")

            replaceFunc.append(
                lambda x: re.sub(
                    reg,
                    lambda text: "%s%s%s%s" % (
                        self.colors.get(color, ""),
                        self.styles.get(style, ""),
                        text.group(0),
                        "\033[0m",
                    ),
                    x,
                )
            )

        head = flags.int("-n", -1)
        tail = flags.int("-t", -1)
        follow = flags.bool("-f")
        file = flags.string("_")
        if file == "":
            debug("read from stdin")
            for line in sys.stdin:
                text = line
                for r in replaceFunc:
                    text = r(text)
                sys.stdout.write(text)
        else:
            debug("read from file", file)
            with open(file, "r") as f:
                lines = f.readlines()
                if head != -1:
                    lines = lines[: min(head, len(lines))]
                if tail != -1:
                    lines = lines[max(-len(lines), -tail):]
                for line in lines:
                    text = line
                    for r in replaceFunc:
                        text = r(text)
                    sys.stdout.write(text)
                while follow:
                    try:
                        text = f.readline()
                    except:
                        break
                    for r in replaceFunc:
                        text = r(text)
                    sys.stdout.write(text)

    def parse(self, repl, text):
        return text if re.match(repl, text) != None else None

    def get(self, params):
        pass


addons.append(Colorful)
