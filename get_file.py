from tkinter import filedialog

file = filedialog.askopenfilename(initialdir="/Users/catalyst/Library/Application Support/Martian Rex, Inc_/Stone Story/", filetypes=[("save file", "*.txt")])
print(file, end="")
