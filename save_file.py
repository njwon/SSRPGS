from tkinter import filedialog
from os import remove
from sys import argv

# from setup import *

# Get path and filename
trace = argv[1].split('/')
initialdir = '/'.join(trace[:-1])
initialfile = trace[-1]
defaultextension = trace[-1].split('.')[-1]

file = filedialog.asksaveasfile(
    initialfile=initialfile,
    initialdir=initialdir,
    defaultextension=defaultextension,
    confirmoverwrite=False,
)

if file is not None:
    # Delete touched file
    file.close()
    remove(file.name)

    print(file.name, end="")
else:
    print("", end="")
