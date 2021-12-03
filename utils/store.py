from .context import ctx

import os


def kvStore(key, value):
    with open(os.path.join(ctx.root, 'store', key), "w") as f:
        f.write(value)


def kvLoad(key, default=""):
    filepath = os.path.join(ctx.root, 'store', key)
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return f.read()
    else:
        return default
