import dearpygui.dearpygui as dpg

from tools.setup import *
from tools.utils import add_help

# Time regex
# \d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}
# MM.DD.YYYY HH:MM:SS

class TimesTab:
    def __init__(self, save):
        self.save = save
        self.progress_data = None

    def load(self):
        self.progress_data = self.save["progress_data"]
        self.trearuse_factory = self.save["progress_data"]["treasure_factory"]
        self.quest_data = self.save["progress_data"]["quest_data"]

        # Crypt intro
        dpg.configure_item(
            "nextTreasureAvailableDate",
            default_value=self.save["progress_data"]["crypt_intro"]["nextTreasureAvailableDate"]
        )

        # Treasure factory
        for value in ("uniqueDate", "crystalDate", "goldDate"):
            dpg.configure_item(value, default_value=self.trearuse_factory[value])

        # Active offline run
        dpg.delete_item("active_run", children_only=True)
        if "activeRun" in self.quest_data:
            with dpg.group(parent="active_run"):
                dpg.add_separator()
                dpg.add_text(i18n["active_offline_run"])

                active_run = self.quest_data["activeRun"]

                dpg.add_input_text(
                    label=i18n["location"],
                    default_value=active_run["questId"],
                    callback=self.change,
                    user_data=("quest_data", "activeRun", "questId")
                )
                dpg.add_input_int(
                    label=i18n["difficulty"],
                    default_value=active_run["difficulty"],
                    callback=self.change,
                    user_data=("quest_data", "activeRun", "difficulty")
                )
                dpg.add_input_int(
                    label=i18n["treasures_per_cycle"],
                    default_value=active_run["treasuresPerLoop"],
                    callback=self.change,
                    user_data=("quest_data", "activeRun", "treasuresPerLoop")
                )
                dpg.add_input_text(
                    label=i18n["start_time"],
                    default_value=active_run["startTime"],
                    callback=self.change,
                    user_data=("quest_data", "activeRun", "startTime")
                )
                dpg.add_input_int(
                    label=i18n["seed"],
                    default_value=active_run["seed"],
                    callback=self.change,
                    user_data=("quest_data", "activeRun", "seed")
                )
        
        # Rewards
        dpg.delete_item("rewards", children_only=True)
        with dpg.group(parent="rewards"):
            if "lastRewardTime" in self.quest_data \
            or "skullnata" in self.quest_data:
                dpg.add_separator()
                dpg.add_text(i18n["rewards"])

            if "lastRewardTime" in self.quest_data:
                dpg.add_input_text(
                    label=i18n["last_reward_time"],
                    default_value=self.save["progress_data"]["quest_data"]["lastRewardTime"],
                    callback=self.change,
                    user_data=("quest_data", "lastRewardTime")
                )
                add_help(i18n["last_reward_time_cheating_info"])

            if "skullnata" in self.save["progress_data"]["quest_data"]:
                dpg.add_input_text(
                    label=i18n["skullnata"],
                    default_value=self.save["progress_data"]["quest_data"]["skullnata"],
                    callback=self.change,
                    user_data=("quest_data", "skullnata")
                )

    def change(self, _, value, path):
        head = self.progress_data
        for key in path[:-1]:
            head = head[key]

        head[path[-1]] = value

        print(f"Changed field: {path[-1]}: {head[path[-1]]}")

    def gui(self):
        with dpg.child_window(
            no_scrollbar=True,
            border=False
        ):
            dpg.add_text(i18n["treasure_factory"])
            dpg.add_input_text(
                label=i18n["unique_date"],
                tag="uniqueDate",
                callback=self.change,
                user_data=("treasure_factory", "uniqueDate")
            )
            dpg.add_input_text(
                label=i18n["crystal_date"],
                tag="crystalDate",
                callback=self.change,
                user_data=("treasure_factory", "crystalDate")
            )
            dpg.add_input_text(
                label=i18n["gold_date"],
                tag="goldDate",
                callback=self.change,
                user_data=("treasure_factory", "goldDate")
            )

            dpg.add_separator()
            dpg.add_text(i18n["locations"]["undead_crypt_intro"])
            dpg.add_input_text(
                label=i18n["next_treasure"],
                tag="nextTreasureAvailableDate",
                callback=self.change,
                user_data=("crypt_intro", "nextTreasureAvailableDate")
            )

            dpg.add_group(tag="rewards")

            dpg.add_group(tag="active_run")
