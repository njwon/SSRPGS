import dearpygui.dearpygui as dpg

from utils import add_help

class MainTab:
    def __init__(self, save):
        self.save = save
        self.progress_data = None

    def load(self):
        self.progress_data = self.save["progress_data"]

        dpg.configure_item("version", default_value=self.progress_data["version"])
        dpg.configure_item("player_name", default_value=self.progress_data["hero_settings"]["playerName"])
        dpg.configure_item("player_level", default_value=self.progress_data["xp"]["currentLevel"])
        dpg.configure_item("player_xp", default_value=self.progress_data["xp"]["currentXP"])

        for resource in ("Stone", "Wood", "Tar", "Xi", "Bronze"):
            if resource not in self.save["progress_data"]["inventory_data"]:
                self.save["progress_data"]["inventory_data"][resource] = 0
            
            dpg.configure_item(resource, default_value=self.save["progress_data"]["inventory_data"][resource])

    def change(self, _, value, path):
        # Pointer on last object inside of a dict
        head = self.progress_data
        for key in path[:-1]:
            head = head[key]

        head[path[-1]] = value

        print(f"Changed field: {path[-1]}: {head[path[-1]]}")

    def gui(self):
        dpg.add_text("Персонаж")

        dpg.add_input_text(label="Версия сохранения", tag="version", callback=self.change, user_data=["version"])
        dpg.add_input_text(label="Имя персонажа", tag="player_name", callback=self.change, user_data=["hero_settings", "playerName"])
        dpg.add_input_int(label="Уровень персонажа", tag="player_level", callback=self.change, user_data=["xp", "currentLevel"])
        add_help("Влияет на предел подбора сундуков:\nlimit = 100 + 5 * player_level")
        dpg.add_input_int(label="Очки опыта", tag="player_xp", callback=self.change, user_data=["xp","currentXP"])

        dpg.add_separator()
        dpg.add_text("Ресурсы")

        dpg.add_input_int(label="Камни    o", tag="Stone", callback=self.change, user_data=( "inventory_data", "Stone"))
        dpg.add_input_int(label="Дерево  _/`", tag="Wood", callback=self.change, user_data=( "inventory_data", "Wood"))
        dpg.add_input_int(label="Смола    ≈", tag="Tar", callback=self.change, user_data=( "inventory_data", "Tar"))
        dpg.add_input_int(label="Ки       @", tag="Xi", callback=self.change, user_data=( "inventory_data", "Xi"))
        dpg.add_input_int(label="Бронза   :.", tag="Bronze", callback=self.change, user_data=( "inventory_data", "Bronze"))
