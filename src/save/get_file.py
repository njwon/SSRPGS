from getpass import getuser
from tkinter import filedialog
from os import path, name

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
    initialdir=initialdir,
    filetypes=[
        ("save file", "*.txt"),
        ("json file", "*.json"),
    ]
)

print(file, end="")
