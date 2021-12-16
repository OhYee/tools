# -*- coding:utf-8 -*-

"""
Python2/3 兼容，输入参数处理
"""

import sys


class Flags:
    """
    Flags 解析命令行参数类参数
    """

    def __init__(self, usage="", argv=None):
        """
        - usage: 最前面的帮助文档
        - argv: 参数列表 list(str)
        """
        self.argv = sys.argv[1:] if argv == None else argv

        self.options = []
        self.optionMap = {}
        self.usage = usage
        self.shortOpt = {}

        self.ret = {}
        self.parsed = False

    def addOption(self, option="", help="", hasValue=False):
        """
        添加一个参数选项
        - flag: 用于识别的选项，如 ["-h", "--help"]
        - help: 对应的帮助说明
        - hasValue: 是否要将后一个参数作为当前参数的值
        """
        if type(option) != list:
            option = [option]

        fid = len(self.options)
        temp = []
        for f in option:
            if type(f) == str and f != "":
                temp.append(f)
                self.optionMap[f] = fid
                if len(f) == 2 and f[0] == "-":
                    self.shortOpt[f[1]] = fid
        self.options.append({
            "flag": temp,
            "help": help,
            "hasValue": hasValue,
            "id": fid,
        })

    def addCommand(self, command="", help="", hasValue=False):
        """
        添加一个参数选项
        - flag: 用于识别的选项，如 ["-h", "--help"]
        - help: 对应的帮助说明
        - hasValue: 是否要将后一个参数作为当前参数的值
        """
        if type(command) != list:
            command = [command]

        fid = len(self.options)
        temp = []
        for f in command:
            if type(f) == str and f != "":
                temp.append(f)
                self.optionMap[f] = fid
                if len(f) == 2 and f[0] == "-":
                    self.shortOpt[f[1]] = fid
        self.options.append({
            "flag": temp,
            "help": help,
            "hasValue": hasValue,
            "id": fid,
        })

    def parse(self):
        """
        解析参数
        """
        if self.parsed:
            return self.ret

        argv = self.argv
        restArgv = []
        ret = {}
        skip = False

        for idx, arg in enumerate(argv):
            if skip:
                skip = False
                continue

            if arg in self.optionMap:
                # 如果存在对应选项，则进行解析
                fid = self.optionMap[arg]
                flag = self.options[fid]
                value = True
                if flag.get("hasValue", False) and idx + 1 < len(argv):
                    # 如果存在值，则将下一个参数跳过
                    value = argv[idx + 1]
                    skip = True
                if fid not in ret:
                    ret[fid] = []
                ret[fid].append(value)
            elif len(arg) > 2 and arg[0] == "-" and arg[1] != "-":
                # 如果是形如 -it 的选项，则尝试将其解析为 -i 和 -t
                args = list(arg[1:])
                fids = [
                    self.optionMap.get("-%s" % arg, -1)
                    for arg in args
                ]
                if len([fid for fid in fids if fid == -1]) > 0:
                    restArgv.append(arg)
                else:
                    for fid in fids:
                        ret[fid].append(True)
            else:
                # 未知选项
                restArgv.append(arg)

        for key, value in ret.items():
            flag = self.options[key]
            for f in flag.get("flag", []):
                self.ret[f] = value
        self.ret["_"] = restArgv
        self.parsed = True
        return self.ret

    def help(self):
        """
        返回帮助文档
        """
        line = [
            (
                " ".join(flag.get("flag", [])) +
                (" [value]" if flag.get("hasValue", False) else ""),
                flag["help"],
            )
            for flag in self.options
        ]

        result = [
            sys.argv[0] if len(self.usage) == 0 else self.usage,
            "",
            "options:",
            align(line)
        ]

        return "\n".join(result)

    def showHelp(self):
        """
        显示帮助文档并退出
        """
        print(self.help())
        exit(0)

    def list(self, key):
        """
        返回指定选项列表
        """
        self.parse()
        return self.ret.get(key, [])

    def count(self, key):
        """
        返回指定选项出现的次数
        """
        return len(self.list(key))

    def bool(self, key):
        """
        返回是否出现过指定选项
        """
        return self.count(key) > 0

    def string(self, key):
        """
        返回指定选项的值（第一个）
        """
        lst = self.list(key)
        return lst[0] if len(lst) > 0 else ""

    def int(self, key, default=0):
        """
        返回指定选项的值（第一个），并转换为整数
        """
        try:
            n = int(self.string(key))
        except:
            n = default
        return n

    def restArgs(self):
        """
        返回解析失败的参数
        """
        return self.list("_")


if __name__ == "__main__":
    flags = Flags(
        "%s -v -v -v -b -vb -f 1.txt -f 2.txt lovelive super star" % sys.argv[0]
    )
    flags.addOption(
        ["-h", "--help"],
        "show help",
    )
    flags.addOption(
        ["-v", "--verbose"],
        "verbose",
    )
    flags.addOption(
        ["-f", "--file"],
        "open files",
        True
    )
    flags.addOption(
        ["-b", "--base64"],
        "base64",
    )

    print(flags.parse())
    flags.showHelp()
    print("never print")


def align(text, tab=4):
    if len(text) == 0:
        return ""
    tab = tab*" "
    maxLen = max([len(x[0]) for x in text])
    result = [
        tab + x[0].ljust(maxLen) + tab + " ".join(x[1:])
        for x in text
    ]
    return "\n".join(result)
