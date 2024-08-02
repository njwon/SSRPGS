from getpass import getuser
from tkinter import filedialog

# TODO: Windows save folder location
initialdir = f"/Users/{getuser()}/Library/Application Support/Martian Rex, Inc_/Stone Story/"

file = filedialog.askopenfilename(
    initialdir=initialdir,
    filetypes=[
        ("save file", "*.txt"),
        ("json file", "*.json"),
    ]
)

print(file, end="")
