import dearpygui.dearpygui as dpg
from utils import add_help
from translations import *

class MainTab:
    def __init__(self, save):
        self.save = save
        self.progress_data = None

    def load(self):
        self.progress_data = self.save["progress_data"]

        # Player info
        dpg.configure_item(
            "player_name",
            default_value=self.progress_data["hero_settings"]["playerName"]
        )
        dpg.configure_item(
            "player_level",
            default_value=self.progress_data["xp"]["currentLevel"]
        )
        dpg.configure_item(
            "player_xp",
            default_value=self.progress_data["xp"]["currentXP"]
        )

        # Resources
        for resource in ("Stone", "Wood", "Tar", "Xi", "Bronze"):
            dpg.configure_item(resource, show=False)
            if resource in self.save["progress_data"]["inventory_data"]:
                dpg.configure_item(
                    resource,
                    show=True,
                    default_value=self.save["progress_data"]["inventory_data"][resource]
                )

    def change(self, _, value, path):
        # Pointer on last object inside of a dict
        head = self.progress_data
        for key in path[:-1]:
            head = head[key]

        head[path[-1]] = value

        print(f"Changed field: {path[-1]}: {head[path[-1]]}")

    def gui(self):
        with dpg.child_window(
            border=False,
            no_scrollbar=True
        ):            
            dpg.add_text(i18n["player"])
            dpg.add_input_text(
                label=i18n["name"],
                tag="player_name",
                callback=self.change,
                user_data=["hero_settings", "playerName"]
            )
            dpg.add_input_int(
                label=i18n["level"],
                tag="player_level",
                callback=self.change,
                user_data=["xp", "currentLevel"]
            )
            add_help(i18n["max_afk_chests_info"])
            dpg.add_input_int(
                label=i18n["xp"],
                tag="player_xp",
                callback=self.change,
                user_data=["xp","currentXP"]
            )

            dpg.add_separator()
            dpg.add_text(i18n["resources"])
            dpg.add_input_int(
                label=i18n["stone"],
                tag="Stone",
                callback=self.change,
                user_data=("inventory_data", "Stone")
            )
            dpg.add_input_int(
                label=i18n["wood"],
                tag="Wood",
                callback=self.change,
                user_data=("inventory_data", "Wood")
            )
            dpg.add_input_int(
                label=i18n["tar"],
                tag="Tar",
                callback=self.change,
                user_data=("inventory_data", "Tar")
            )
            dpg.add_input_int(
                label=i18n["ki"],
                tag="Xi",
                callback=self.change,
                user_data=("inventory_data", "Xi")
            )
            dpg.add_input_int(
                label=i18n["bronze"],
                tag="Bronze",
                callback=self.change,
                user_data=("inventory_data", "Bronze")
            )
