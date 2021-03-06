# -*- coding:utf-8 -*-

from addon import addons
from utils import *
import os

i18n = {
    "zh_CN": {
        "show_help": "显示帮助",
        "debug_mode": "测试模式",
    },
    "en_US": {
        "show_help": "show help",
        "debug_mode": "debug mode",
    },
}

if __name__ == "__main__":
    lang = I18n(i18n)

    flags = Flags("o [command] [options]")
    flags.addOption(["-h", "--help"], lang.get("show_help"))
    flags.addOption(["-d", "--debug"], lang.get("debug_mode"))

    ctx.debug = flags.bool("-d")
    ctx.help = flags.bool("-h")
    ctx.root = os.path.split(os.path.realpath(__file__))[0]

    debug(flags.parse())
    debug(ctx)

    commands = []
    for addon in addons:
        add = addon()

        temp = add.name()
        if type(temp) != list:
            temp = [temp]

        names = []
        for name in temp:
            debug(name, type(name))
            if type(name) == str:
                names.append(name.replace(" ", "").lower())
        commands.append(
            (
                add,
                names,
                add.description()
            )
        )

    debug("addon loaded:", commands)

    rargs = flags.restArgs()
    command = rargs[0] if len(rargs) > 0 else ""
    if command != "":
        for cmd in commands:
            if command in cmd[1]:
                debug("run %s %s" % (command,  cmd[1]))
                try:
                    cmd[0].run(rargs[1:])
                except KeyboardInterrupt:
                    pass
                exit(0)
        stdoutLine("Unknown command: %s" % command)

    stdoutLine("\n".join([
        flags.help(),
        "",
        "commands:",
        align([
            (",".join(cmd[1]), cmd[2])
            for cmd in commands
        ])
    ]))
    exit(0)
