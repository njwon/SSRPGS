from tkinter import filedialog
from getpass import getuser

filetypes = [
    ("Save file", "*.txt"),
    ("Json file", "*.json")
]

initialdir = (
    f"/Users/{getuser()}/Library/"
    "Application Support/Martian Rex, Inc_/Stone Story/"
)

save_file = filedialog.askopenfilename(
    filetypes=filetypes,
    initialdir=initialdir
)

print(save_file, end="")
