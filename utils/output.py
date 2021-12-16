# -*- coding:utf-8 -*-

from .context import ctx
import sys


def debug(*args):
    if ctx.debug:
        print(" ".join(map(str, args)))


def stdout(*args, end="\n"):
    sys.stdout.write(" ".join(map(str, args)))
    sys.stdout.write(end)
    sys.stdout.flush()


def stderr(*args, end="\n"):
    sys.stderr.write(" ".join(map(str, args)))
    sys.stderr.write(end)
    sys.stderr.flush()
