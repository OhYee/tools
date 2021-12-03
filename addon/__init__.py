import os
from .base import addons

addon_dir = os.path.split(os.path.realpath(__file__))[0]

for _, _, files in os.walk(addon_dir):
    for file in files:
        if file.endswith(".py") and file != "base.py" and file != "__init__.py":
            exec("from .%s import *" % file[:-3])
