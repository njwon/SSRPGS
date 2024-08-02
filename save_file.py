from tkinter import filedialog
from sys import argv

# Get path and filename
trace = argv[1].split('/')
initialdir = '/'.join(trace[:-1])
initialfile = '.'.join(trace[-1].split('.')[:-1])

file = filedialog.asksaveasfile(
    initialfile=initialfile,
    initialdir=initialdir,
    defaultextension=".txt",
    filetypes=[
        ("save file", "*.txt"),
        ("json file", "*.json"),
    ]
)

if file is not None:
    print(file.name, end="")
else:
    print("", end="")
