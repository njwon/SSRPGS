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

from utils import loading

class Editor:
    def __init__(self):
        self.init_dpg()
        self.init_font()

        self.save = Save()

        # settings_tab
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
                dpg.add_font_range(0x10ec77, 0x10ffff)
                for char in range(0x10ec77, 0x10ffff):
                    dpg.add_char_remap(char, ord(" "))
                
                dpg.bind_font(font)

    def load(self):
        save_file = check_output([executable, "get_file.py"])  # I don't know what's wrong with dpg
        
        if not save_file:
            return

        with loading():
            self.save.open(save_file)

        dpg.configure_item(
            "save_slots",
            items=self.save.save_slots,
            default_value=self.save.save_slot
        )
        
        # Load data to tabs
        self.main_tab.load()
        self.locations_tab.load()
        self.inventory_tab.load()
        self.cosmetics_tab.load()
        self.quests_tab.load()
        self.progress_tab.load()
        self.times_tab.load()

    def dump(self):
        with loading():
            self.save.save("primary_save.txt")

    def change_slot(self, _, new_save_slot):
        self.save.save_slot = new_save_slot

        # Sync values to fields
        self.main_tab.load()
        self.progress_tab.load()
        self.locations_tab.load()
        self.inventory_tab.load()
        self.cosmetics_tab.load()
        self.quests_tab.load()
        self.times_tab.load()

    def json_export(self):
        self.save.save_as_json("formatted.json")
    
    def json_import(self):
        self.save.open_from_json("formatted.json")
        
        self.change_slot("", self.save.save_slot)

        dpg.configure_item(
            "save_slots",
            items=self.save.save_slots,
            default_value=self.save.save_slot
        )
        
        # Load data to tabs
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
            with dpg.group(horizontal=True):
                dpg.add_button(label="Открыть", callback=self.load)
                dpg.add_button(label="Сохранить", callback=self.dump)
                dpg.add_combo(label="Слот сохранения", width=300, items=[], callback=self.change_slot, tag="save_slots")
                
            # Tabs
            with dpg.tab_bar():
                with dpg.tab(label="Настройки"):
                    dpg.add_text("Stone Story RPG save editor\nv 0.0.0")
                    dpg.add_button(label="Экспортировать JSON", callback=self.json_export)
                    dpg.add_button(label="Импортировать JSON", callback=self.json_import)

                with dpg.tab(label="Общее"):
                    self.main_tab.gui()

                with dpg.tab(label="Прогресс"):
                    self.progress_tab.gui()

                with dpg.tab(label="Локации"):
                    self.locations_tab.gui()

                with dpg.tab(label="Инвентарь"):
                    self.inventory_tab.gui()

                with dpg.tab(label="Косметика"):
                    self.cosmetics_tab.gui()

                with dpg.tab(label="Квесты"):
                    self.quests_tab.gui()

                with dpg.tab(label="Время"):
                    self.times_tab.gui()

    def run(self):
        self.gui()

        dpg.create_viewport(
            title="Редактор сохранений Stone Story RPG",
            width=600,
            height=398,
        )
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Editor", True)
        dpg.start_dearpygui()
        dpg.destroy_context()

editor = Editor()
editor.run()
