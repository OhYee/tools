# -*- coding:utf-8 -*-

from .base import *
from utils import *

import json
import re

_DEFAULT_JSON_INDENT = 2
i18n = {
    "zh_CN": {
        "description": "JSON 人类友好输出",
        "indent_help": "缩进格数，默认 %d" % _DEFAULT_JSON_INDENT,
        "highlight_help": "高亮",
        "ascii_help": "只显示 ASCII 字符"
    },
    "en_US": {
        "description": "Human-friendly JSON output",
        "indent_help": "text indent, default %d" % _DEFAULT_JSON_INDENT,
        "highlight_help": "enable highlight",
        "ascii_help": "only show ascii"
    },
}


class JSON(Addon):
    def __init__(self):
        debug("Init JSON", ctx)
        self.lang = I18n(i18n)

    def name(self):
        return ["jq", "json"]

    def description(self):
        return self.lang.get("description")

    def run(self, params):
        flags = Flags("o json [command] [options]", params)
        flags.addOption(
            ["-c", "--color", "--highlight"],
            self.lang.get("highlight_help"),
            False,
        )
        flags.addOption(
            ["-i", "--indent"],
            self.lang.get("indent_help"),
            True,
        )
        flags.addOption(
            ["-a", "--ascii"],
            self.lang.get("ascii_help"),
            False,
        )
        debug(flags.parse())

        if ctx.help:
            flags.showHelp()

        text = stdin()
        try:
            jsonObj = json.loads(text)
            jsonText = json.dumps(
                jsonObj,
                indent=flags.int("-i", _DEFAULT_JSON_INDENT),
                ensure_ascii=flags.bool("-a")
            )

            if flags.bool("-c"):
                # number
                jsonText = re.sub(
                    r'(\d+)(?=,|\r|\n)',
                    lambda m: "\033[33m%s\033[0m" % (m.groups(0)[0]),
                    jsonText,
                )

                # string
                jsonText = re.sub(
                    r'((?<!\\)".*(?<!\\)")',
                    lambda m: "\033[32m%s\033[0m" % (m.groups(0)[0]),
                    jsonText,
                )

            stdoutLine(jsonText)
        except Exception as e:
            stderrLine(e)
            stdoutLine(text)

    def parse(self, repl, text):
        return text if re.match(repl, text) != None else None

    def get(self, params):
        pass


addons.append(JSON)
