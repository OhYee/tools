# -*- coding:utf-8 -*-

from .context import ctx
import sys


def debug(*args):
    if ctx.debug:
        print(" ".join(map(str, args)))


def stdout(*args):
    sys.stdout.write(" ".join(map(str, args)))
    sys.stdout.flush()


def stdoutLine(*args):
    stdout(*args)
    stdout("\n")
    sys.stdout.flush()


def stderr(*args):
    sys.stderr.write(" ".join(map(str, args)))
    sys.stderr.flush()


def stderrLine(*args):
    stderr(*args)
    stderr("\n")
    sys.stderr.flush()
