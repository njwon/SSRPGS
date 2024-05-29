# demo.py
import dearpygui.dearpygui as dpg
from tkinter import filedialog

dpg.create_context()

def open_file():
    file = filedialog.askopenfilename()  # Gives trace trap
    print(f"{file=}")

with dpg.window(tag="Demo"):
    dpg.add_button(label="Open file", callback=open_file)

dpg.create_viewport(title="Demo", width=600, height=412)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Demo", True)
dpg.start_dearpygui()
dpg.destroy_context()
