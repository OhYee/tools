# -*- coding:utf-8 -*-

class _ctx():
    def __init__(self):
        self.debug = False
        self.help = False
        self.ctx = "."

    def __str__(self):
        return "ctx[%s]" % ", ".join(
            ["%s=%s" % (arg, getattr(self, arg))
                for arg in dir(self)
                if not callable(getattr(self, arg)) and not (len(arg) > 1 and arg[0] == "_")
             ]
        )


ctx = _ctx()
