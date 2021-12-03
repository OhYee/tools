# -*- coding:utf-8 -*-

from .context import ctx


def debug(*args):
    if ctx.debug:
        print(" ".join(map(str, args)))
