import dearpygui.dearpygui as dpg

from subprocess import check_output
from sys import executable

from save import Save

from main_tab import MainTab
from locations_tab import LocationsTab
from inventory_tab import InventoryTab
from cosmetics_tab import CosmeticsTab
from progress_tab import ProgressTab
from quests_tab import QuestsTab
from times_tab import TimesTab

from translations import *
from utils import loading, add_help

REMAP_START = 0x10ec77
REMAP_END = 0x10ffff

class Editor:
    def __init__(self):
        self.init_dpg()
        self.init_font()

        self.save = Save()

        self.main_tab = MainTab(self.save)
        self.progress_tab = ProgressTab(self.save)
        self.locations_tab = LocationsTab(self.save)
        self.inventory_tab = InventoryTab(self.save)
        self.cosmetics_tab = CosmeticsTab(self.save)
        self.quests_tab = QuestsTab(self.save)
        self.times_tab = TimesTab(self.save)

    def init_dpg(self):
        dpg.create_context()

    def init_font(self):
        with dpg.font_registry():
            with dpg.font("mononoki-Regular.ttf", 32) as font:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
                dpg.add_font_chars([ord(c) for c in "♦≈★"])
                dpg.set_global_font_scale(0.5)

                # Adds ~7,5 millisecond to init time...
                # Remap 5k of Unicode chars to indexes for inventory tab
                dpg.add_font_range(REMAP_START, REMAP_END)
                for char in range(REMAP_START, REMAP_END):
                    dpg.add_char_remap(char, ord(" "))

                dpg.bind_font(font)

    def load(self):
        save_file = check_output(
            [executable, "get_file.py"]
        )  # I don't know what's wrong with dpg

        save_file = str(save_file, encoding="utf-8")
        print(f"Gathered save file {save_file}")

        if save_file.endswith(".txt"):
            print("Loading as .txt")
            with loading():
                self.save.open(save_file)

        elif save_file.endswith(".json"):
            print("Loading as .json")
            self.save.open_from_json("formatted.json")
        
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

        save_file = check_output(
            [executable, "save_file.py", self.save.save_file_name]
        )  # I don't know what's wrong with dpg

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
                    width=135,
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

                        dpg.add_separator()
                        dpg.add_text(i18n["settings"])
                        dpg.add_combo(
                            label=i18n["language"],
                            default_value=i18n["language-name"],
                            items=list(languages.values()),
                            callback=configure_language
                        )
                        add_help(i18n["language_info"])

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
        self.gui()

        dpg.create_viewport(
            title=i18n["title"],
            width=600,
            height=394,
            small_icon="icon.ico",
            resizable=False
        )
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Editor", True)
        dpg.start_dearpygui()
        dpg.destroy_context()

editor = Editor()
editor.run()
