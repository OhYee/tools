import os
from .base import addons

addon_dir = os.path.split(os.path.realpath(__file__))[0]

for dir, _, files in os.walk(addon_dir):
    for file in files:
        if file.endswith(".py") and file != "base.py" and file != "__init__.py":
            if dir != addon_dir:
                file = dir[len(addon_dir)+1:] + "/" + file
            file = file[:-3].replace("/", ".")
            exec("from .%s import *" % file)
