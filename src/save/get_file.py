from tkinter import filedialog
from getpass import getuser
from os import path, name

import tomllib

with open("settings.toml", "rb") as f:
    settings = tomllib.load(f)

    if settings["upscale"]:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(2)

if name == "nt":
    initialdir = path.join(
        path.expandvars('%USERPROFILE%'),
        'AppData/LocalLow/Martian Rex, Inc_/Stone Story/'
    )
else:
    initialdir = (
        f"/Users/{getuser()}/Library/"
        "Application Support/Martian Rex, Inc_/Stone Story/"
    )

file = filedialog.askopenfilename(
    filetypes=[
        ("Save file", "*.txt"),
        ("Json file", "*.json")
    ],
    initialdir=initialdir
)

print(file, end="")
