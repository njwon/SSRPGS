import dearpygui.dearpygui as dpg
from translations import *

available_locations = (
    "temple",
    "cross_bridge",
    "icy_ridge",
    "bronze_gate",
    "bronze_mine",
    "cross_deadwood_river",
    "undead_crypt",
    "undead_crypt_intro",
    "uulaa_shop",
    "mushroom_shop",
    "fungus_forest",
    "waterfall",
    "caustic_caves",
    "deadwood_valley",
    "rocky_plateau",
)

available_workbench = (
    "mutate",
    "automate",
    "fuse_enchantments",
    "break_apart_items",
    "brew_potion",
    "anvil",
)

legends = (
    "epic_croaked",
    "epic_roof_overhead",
    "epic_bad_business",
    "epic_throwing_stones",
    "epic_wild_ride",
    "epic_remnants_five",
    "epic_ascension",
    "epic_titanic_accord",
    "epic_smack_hammer",
    "epic_cauldron_collective",
    "epic_initiate",
    "epic_blowing_steam",
    "epic_head_over_heels",
    "epic_transmutable_trials",
    "epic_burnout",
)

# TODO: Realize wtf it should be there
TODO = (
    "find_shelter",
    "rocky_plateau",
    "build_door",
    "deadwood_valley",
    "build_workstation",
    "craft_shovel",
    "craft_hatchet",
    "prospect_cliff",
    "clean_sword",
    "upgrade_workstation_2",
    "craft_canoe",
    "dig_cave",
    "caustic_caves",
    "craft_anvil_hammer",
    "craft_anvil",
    "anvil",
    "cross_deadwood_river",
    "bronze_gate",
    "upgrade_workstation_3",
    "craft_grappling_hook",
    "utility_belt",
    "waterfall",
    "fungus_forest",
    "undead_crypt_intro",
    "undead_crypt",
    "bronze_mine",
    "upgrade_workstation_4",
    "make_cauldron",
    "icy_ridge",
    "break_apart_items",
    "make_fire_pit",
    "light_fire",
    "cauldron_fetch_water",
    "brew_potion",
    "upgrade_cauldron",
    "broken_bridge",
    "fuse_enchantments",
    "make_planks",
    "fix_bridge",
    "cross_bridge",
    "temple",
    "automate",
    "make_bowl",
    "mutate",
    "fetch_water",
    "prepare_paint",
    "make_paintbrush",
    "upgrade_ouroboros",
    "upgrade_star_stone",
    "fetch_water_yellow",
    "prepare_paint_yellow",
    "craft_fishing_rod",
    "craft_goal_book",
    "craft_grappling_hook_lv2",
    "mushroom_shop",
    "uulaa_shop"
)

all_quests = available_locations + available_workbench

class ProgressTab:
    def __init__(self, save):
        self.save = save
        self.quests = None
        self.legends = None

    def load(self):
        if "records" not in self.save["progress_data"]["custom_quests"]:
            self.save["progress_data"]["custom_quests"]["records"] = []

        self.quests = self.save["progress_data"]["quest_data"]["available"]
        self.legends = self.save["progress_data"]["custom_quests"]["revealed"]
        self.records = self.save["progress_data"]["custom_quests"]["records"]

        all_locations_opened = all([quest in self.quests for quest in available_locations])
        all_workbench_opened = all([quest in self.quests for quest in available_workbench])
        all_legends_opened = all([legend in self.legends for legend in legends])

        dpg.configure_item("all_locations", default_value=all_locations_opened)
        dpg.configure_item("all_workbench", default_value=all_workbench_opened)
        dpg.configure_item("all_legends", default_value=all_legends_opened)

        for quest in all_quests:
            dpg.configure_item(quest, default_value=quest in self.quests)

        for legend in legends:
            dpg.configure_item(legend, default_value=legend in self.legends)

    def switch(self, _, value, quest):
        if not self.save.is_loaded():
            return

        if value and quest not in self.quests:
            self.quests.append(quest)
            print(f"Opened {quest}")

        if not value and quest in self.quests:
            self.quests.pop(self.quests.index(quest))
            print(f"Closed {quest}")

    def switch_legend(self, _, value, legend):
        if not value and legend in self.legends:
            self.legends.remove(legend)

            for i, legend_data in enumerate(self.records):
                if legend_data["questId"] == legend:
                    self.records[i]["unlocked"] = False
                    print(f"Closed {legend} legend")
                    return

        if value and legend not in self.legends:
            self.legends.append(legend)
            for i, legend_data in enumerate(self.records):
                if legend_data["questId"] == legend:
                    legend_data["unlocked"] = True
                    break
            else:
                self.records.append({
                    "questId": legend,
                    "unlocked": True
                })

            print(f"Opened {legend} legend")

    def switch_all(self, _, value, function_and_values):
        function, values = function_and_values
        if not self.save.is_loaded():
            return

        for quest in values:
            dpg.configure_item(quest, default_value=value)
            function(_, value, quest)

    def gui(self):
        with dpg.child_window(no_scrollbar=True, border=False):
            with dpg.table(header_row=False, resizable=True):
                dpg.add_table_column()
                dpg.add_table_column()

                with dpg.table_row():
                    with dpg.group():
                        dpg.add_text(i18n["locations_"])
                        dpg.add_checkbox(
                            label=i18n["all_locations"],
                            tag="all_locations",
                            callback=self.switch_all,
                            user_data=(self.switch, available_locations)
                        )

                        for quest in available_locations:
                            dpg.add_checkbox(
                                label=i18n["locations"][quest],
                                tag=quest,
                                callback=self.switch,
                                user_data=quest
                            )

                        dpg.add_text(i18n["workbench_"])
                        dpg.add_checkbox(
                            label=i18n["workbench_all"],
                            tag="all_workbench",
                            callback=self.switch_all,
                            user_data=(self.switch, available_workbench)
                        )

                        for quest in available_workbench:
                            dpg.add_checkbox(
                                label=i18n["workbench"][quest],
                                tag=quest,
                                callback=self.switch,
                                user_data=quest
                            )

                    with dpg.group():
                        dpg.add_text(i18n["legends_"])
                        dpg.add_checkbox(
                            label=i18n["legends_all"],
                            tag="all_legends",
                            callback=self.switch_all,
                            user_data=(self.switch_legend, legends)
                        )

                        with dpg.group(parent="legends"):
                            for legend in legends:
                                dpg.add_checkbox(
                                    label=i18n["legends"][legend],
                                    tag=legend,
                                    callback=self.switch_legend,
                                    user_data=legend
                                )
