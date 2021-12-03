# -*- coding:utf-8 -*-

class Addon:
    def __init__(self):
        pass

    def name(self):
        return ["BaseAddon"]

    def description(self):
        return "no help"

    def run(self, params):
        print(params)

    def __repr__(self):
        return "Addon[%s]  %s" % (self.name(), self.description())


addons = []
