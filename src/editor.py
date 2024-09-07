import dearpygui.dearpygui as dpg

from subprocess import check_output
from tkinter import filedialog
from sys import executable
from os import path, remove

from save.save import Save

from tabs.main_tab import MainTab
from tabs.locations_tab import LocationsTab
from tabs.inventory_tab import InventoryTab
from tabs.cosmetics_tab import CosmeticsTab
from tabs.progress_tab import ProgressTab
from tabs.quests_tab import QuestsTab
from tabs.times_tab import TimesTab

from tools.setup import *
from tools.utils import loading, add_help

class Editor:
    def __init__(self):
        self.save = Save()
        self.save.encrypt_saves = settings["encrypt_saves"]

        self.main_tab = MainTab(self.save)
        self.progress_tab = ProgressTab(self.save)
        self.locations_tab = LocationsTab(self.save)
        self.inventory_tab = InventoryTab(self.save)
        self.cosmetics_tab = CosmeticsTab(self.save)
        self.quests_tab = QuestsTab(self.save)
        self.times_tab = TimesTab(self.save)

    def load(self):
        if IS_NT:
            filetypes = [
                ("Save file (.txt)", "*.txt"),
                ("Json file (.json)", "*.json")
            ]

            initialdir = path.join(
                path.expandvars('%USERPROFILE%'),
                'AppData/LocalLow/Martian Rex, Inc_/Stone Story/'
            )
 
            save_file = filedialog.askopenfilename(
                filetypes=filetypes,
                initialdir=initialdir
            )
        else:
            save_file = check_output([
                executable,
                "save/get_file.py"
            ])  # I don't know what's wrong with dpg
            save_file = str(save_file, encoding="utf-8")

        print(f"Gathered save file {save_file}")

        if save_file.endswith(".txt"):
            print("Loading as .txt")
            with loading():
                self.save.open(save_file)

        elif save_file.endswith(".json"):
            print("Loading as .json")
            self.save.open_from_json(save_file)

        else:
            print(f"Loading denied")
            return

        # Update tabs
        dpg.configure_item(
            "save_slots",
            items=self.save.save_slots,
            default_value=self.save.save_slot
        )

        self.change_slot("load", self.save.save_slot)

    def dump(self):
        if not self.save.is_loaded():
            return

        if IS_NT:
            # Get path and filename
            trace = self.save.save_file_name.split('/')

            defaultextension = trace[-1].split('.')[-1]
            initialdir = '/'.join(trace[:-1])
            initialfile = trace[-1]
            filetypes = [
                ("Save file (.txt)", "*.txt"),
                ("Json file (.json)", "*.json")
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
                # Delete touched file
                file.close()
                remove(file.name)

                save_file = file.name
            else:
                save_file = ""

        else:
            save_file = check_output([
                executable,
                "save/save_file.py",
                self.save.save_file_name
            ])  # I don't know what's wrong with dpg
            save_file = str(save_file, encoding="utf-8")

        print(f"Gathered save file {save_file}")

        if save_file.endswith(".txt"):
            with loading():
                self.save.save(save_file)
                print("Saved as .txt")
        elif save_file.endswith(".json"):
            self.save.save_as_json(save_file)
            print("Saved as .json")

    def change_slot(self, _, new_save_slot):
        self.save.save_slot = new_save_slot

        # Sync values in fields
        self.main_tab.load()
        self.progress_tab.load()
        self.locations_tab.load()
        self.inventory_tab.load()
        self.cosmetics_tab.load()
        self.quests_tab.load()
        self.times_tab.load()

    def configure_language(self, _, language):
        for code in languages:
            if languages[code] != language:
                continue

            settings["language"] = code

            self.update_settings()
            print(f"Default language is set to {code}")

    def configure_upscale(self, _, upscale):
        settings["upscale"] = upscale

        self.update_settings()
        print(f"Upscale is set to {upscale}")

    def configure_save_encryption(self,_, encrypt_saves):
        self.save.encrypt_saves = encrypt_saves
        settings["encrypt_saves"] = encrypt_saves

        self.update_settings()
        print(f"Encryptions is set to {encrypt_saves}")

    def update_settings(self):
        with open("settings.toml", "w", encoding="utf-8") as config:
            config.write(f"# Save editor\n")
            config.write(f"encrypt_saves = {str(settings["encrypt_saves"]).lower()}\n")
            config.write(f"\n# Files\n")
            config.write(f"language = \"{settings["language"]}\"\n")
            config.write(f"upscale = {str(settings["upscale"]).lower()}\n")

    def gui(self):
        with dpg.window(tag="Editor"):
            # Header
            with dpg.menu_bar():
                dpg.add_button(
                    label=i18n["open"],
                    callback=self.load
                )
                dpg.add_button(
                    label=i18n["save"],
                    callback=self.dump
                )
                dpg.add_combo(
                    label=i18n["save_slot"],
                    width=135 * SCALE,
                    items=[],
                    callback=self.change_slot,
                    tag="save_slots"
                )

            # Tabs
            with dpg.tab_bar():
                with dpg.tab(label=i18n["major_tab"]):
                    with dpg.child_window(
                        no_scrollbar=True,
                        border=False
                    ):
                        dpg.add_text(i18n["info_label"])
                        dpg.add_text(i18n["info"])

                        # Settings
                        dpg.add_separator()
                        with dpg.table(header_row=False, resizable=True):
                            dpg.add_table_column()
                            dpg.add_table_column()

                            with dpg.table_row():
                                # Editor settings
                                with dpg.group():
                                    dpg.add_text(i18n["settings"])
                                    dpg.add_combo(
                                        label=i18n["language"],
                                        default_value=i18n["language-name"],
                                        items=list(languages.values()),
                                        callback=self.configure_language
                                    )
                                    add_help(i18n["language_info"])

                                    if IS_NT:
                                        dpg.add_checkbox(
                                            label=i18n["double_resolution"],
                                            default_value=settings["upscale"],
                                            callback=self.configure_upscale
                                        )

                                # File settings
                                with dpg.group():
                                    dpg.add_text(i18n["files"])
                                    dpg.add_checkbox(
                                        label=i18n["encrypt_saves"],
                                        default_value=settings["encrypt_saves"],
                                        callback=self.configure_save_encryption
                                    )

                with dpg.tab(label=i18n["main_tab"]):
                    self.main_tab.gui()

                with dpg.tab(label=i18n["progress_tab"]):
                    self.progress_tab.gui()

                with dpg.tab(label=i18n["locations_tab"]):
                    self.locations_tab.gui()

                with dpg.tab(label=i18n["inventory_tab"]):
                    self.inventory_tab.gui()

                with dpg.tab(label=i18n["cosmetics_tab"]):
                    self.cosmetics_tab.gui()

                with dpg.tab(label=i18n["quests_tab"]):
                    self.quests_tab.gui()

                with dpg.tab(label=i18n["times_tab"]):
                    self.times_tab.gui()

    def run(self):
        dpg.create_context()

        init_font()
        init_theme()

        self.gui()

        dpg.create_viewport(
            title=str(i18n["title"]),
            width=WIDTH * SCALE + WIDTH_OFFSET,
            height=HEIGHT * SCALE + HEIGHT_OFFSET,
            small_icon="images/icon.ico",
            x_pos=450 * SCALE,
            y_pos=350 * SCALE
        )

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Editor", True)
        dpg.start_dearpygui()
        dpg.destroy_context()

editor = Editor()
editor.run()
