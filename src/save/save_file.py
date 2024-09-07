from tkinter import filedialog
from os import remove
from sys import argv

# Get path and filename
trace = argv[1].split('/')

defaultextension = trace[-1].split('.')[-1]
initialdir = '/'.join(trace[:-1])
initialfile = trace[-1]
filetypes = [
    ("Save file", "*.txt"),
    ("Json file", "*.json")
]

if defaultextension == "json":
    filetypes.reverse()

file = filedialog.asksaveasfile(
    confirmoverwrite=False,
    defaultextension=defaultextension,
    filetypes=filetypes,
    initialdir=initialdir,
    initialfile=initialfile
)

if file is not None:
    remove(file.name)  # Delete touched file
    print(file.name, end="")
else:
    print("", end="")
