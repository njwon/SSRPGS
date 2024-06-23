import dearpygui.dearpygui as dpg

from utils import add_help

class MainTab:
    def __init__(self, save):
        self.save = save
        self.init_registry()

    def load(self):
        dpg.set_value("version", self.save["version"])
        dpg.set_value("player_name", self.save["player_name"])
        dpg.set_value("player_level", self.save["player_level"])
        dpg.set_value("player_xp", self.save["player_xp"])

        for resource in ("Stone", "Wood", "Tar", "Xi", "Bronze"):
            if resource not in self.save["progress_data"]["inventory_data"]:
                self.save["progress_data"]["inventory_data"][resource] = 0
            
            dpg.set_value(resource, self.save["progress_data"]["inventory_data"][resource])

    def dump(self):
        self.save["version"] = dpg.get_value("version")
        self.save["progress_data"]["version"] = dpg.get_value("version")

        self.save["player_name"] = dpg.get_value("player_name")
        self.save["progress_data"]["hero_settings"]["playerName"] = dpg.get_value("player_name")

        self.save["player_level"] = dpg.get_value("player_level")
        self.save["progress_data"]["xp"]["currentLevel"] = dpg.get_value("player_level")

        self.save["player_xp"] = dpg.get_value("player_xp")
        self.save["progress_data"]["xp"]["currentXP"] = dpg.get_value("player_xp")

        for resource in ("Stone", "Wood", "Tar", "Xi", "Bronze"):
            self.save["progress_data"]["inventory_data"][resource] = dpg.get_value(resource)

    def init_registry(self):
        with dpg.value_registry():
            dpg.add_string_value(default_value="", tag="version")
            dpg.add_string_value(default_value="", tag="player_name")
            dpg.add_int_value(default_value=0, tag="player_level")
            dpg.add_int_value(default_value=0, tag="player_xp")

            dpg.add_int_value(default_value=0, tag="Stone")
            dpg.add_int_value(default_value=0, tag="Wood")
            dpg.add_int_value(default_value=0, tag="Tar")
            dpg.add_int_value(default_value=0, tag="Xi")
            dpg.add_int_value(default_value=0, tag="Bronze")

    def gui(self):
        dpg.add_text("Персонаж")

        dpg.add_input_text(label="Версия сохранения", source="version")
        dpg.add_input_text(label="Имя персонажа", source="player_name")
        dpg.add_input_int(label="Уровень персонажа", source="player_level")
        add_help("Влияет на предел подбора сундуков:\nlimit = 100 + 5 * player_level")
        dpg.add_input_int(label="Очки опыта", source="player_xp")

        dpg.add_separator()
        dpg.add_text("Ресурсы")

        dpg.add_input_int(label="Камни    o", source="Stone")
        dpg.add_input_int(label="Дерево  _/`", source="Wood")
        dpg.add_input_int(label="Смола    ≈", source="Tar")
        dpg.add_input_int(label="Ки       @", source="Xi")
        dpg.add_input_int(label="Бронза   :.", source="Bronze")
    