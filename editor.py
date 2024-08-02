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

info = """Файлы сохранения
* primary_save.txt - Основной файл сохранения.
* backup.txt - Резервная копия сохранения, создаваемая игрой.

* Обязательно создавайте резервные ваших сохранений.
* Избыток лишает ценности.

Вы можете экспортировать расшифрованное сохранение как JSON файл,
чтобы получить возможность редактировать все поля данных, а не
только те, что представлены тут.

SSRPGS v1.0.0 by Catalyst
"""

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
                dpg.add_font_range(0x10ec77, 0x10ffff)
                for char in range(0x10ec77, 0x10ffff):
                    dpg.add_char_remap(char, ord(" "))
                
                dpg.bind_font(font)

    def load(self):
        save_file = check_output([executable, "get_file.py"])  # I don't know what's wrong with dpg
        
        if not save_file:
            return

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
        if not self.save.is_loaded():
            return

        save_file = check_output([executable, "save_file.py", self.save.save_file_name])  # I don't know what's wrong with dpg

        save_file = str(save_file, encoding="utf-8")
        print(f"Gathered save file {save_file}")

        if save_file.endswith(".txt"):
            with loading():
                self.save.save(save_file)
                print("Saved as .txt")

        elif save_file.endswith(".json"):
            self.save.save_as_json(save_file)
            print("Saved as .json")

        else:
            print("Saving denied")

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
    
    def gui(self):
        with dpg.window(tag="Editor"):
            # Header
            with dpg.menu_bar():
                dpg.add_menu_item(
                    label="Открыть",
                    callback=self.load
                )
                dpg.add_menu_item(
                    label="Сохранить",
                    callback=self.dump
                )

                # dpg.add_menu_item(label="Импортировать JSON", callback=self.json_import) 
                # dpg.add_menu_item(label="Экспортировать JSON", callback=self.json_export)

                dpg.add_combo(
                    label="Слот сохранения",
                    width=295,
                    items=[],
                    callback=self.change_slot,
                    tag="save_slots"
                )
                
            # Tabs
            with dpg.tab_bar():
                with dpg.tab(label="Главная"):
                    with dpg.child_window(
                        no_scrollbar=True,
                        border=False
                    ):
                        dpg.add_text("Информация")
                        dpg.add_text(info)

                        dpg.add_separator()
                        dpg.add_text("Настройки")
                        dpg.add_combo(
                            items=["Русский", "English"],
                            default_value="Русский",
                            label="Язык",
                            width=100
                        )

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
