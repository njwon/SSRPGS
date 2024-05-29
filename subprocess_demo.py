# subprocess_demo.py
import dearpygui.dearpygui as dpg
from tkinter import filedialog

from sys import executable  # To run subprocess
from subprocess import check_output

dpg.create_context()

def open_file():
    file = check_output([executable, "get_file.py"])  # I don't know what's wrong with dpg
    print(f"{file=}")

with dpg.window(tag="Demo"):
    dpg.add_button(label="Open file", callback=open_file)

dpg.create_viewport(title="Demo", width=600, height=412)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Demo", True)
dpg.start_dearpygui()
dpg.destroy_context()
