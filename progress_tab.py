import dearpygui.dearpygui as dpg

from translations import *

locations = (
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

workbench = (
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

projects = (
    "find_shelter",
    "build_door",
    "build_workstation",
    "craft_shovel",
    "craft_hatchet",
    "prospect_cliff",
    "clean_sword",
    "upgrade_workstation_2",
    "craft_canoe",
    "dig_cave",
    "craft_anvil_hammer",
    "craft_anvil",
    "upgrade_workstation_3",
    "craft_grappling_hook",
    "utility_belt",
    "upgrade_workstation_4",
    "make_cauldron",
    "make_fire_pit",
    "light_fire",
    "cauldron_fetch_water",
    "upgrade_cauldron",
    "broken_bridge",
    "make_planks",
    "fix_bridge",
    "make_bowl",
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
)

class ProgressTab:
    def __init__(self, save):
        self.save = save
        self.quests = None
        self.legends = None
        self.records = None

    def load(self):
        if "records" not in self.save["progress_data"]["custom_quests"]:
            self.save["progress_data"]["custom_quests"]["records"] = []

        self.quests = self.save["progress_data"]["quest_data"]["available"]
        self.legends = self.save["progress_data"]["custom_quests"]["revealed"]
        self.records = self.save["progress_data"]["custom_quests"]["records"]

        all_locations_opened = all([quest in self.quests for quest in locations])
        all_workbench_opened = all([quest in self.quests for quest in workbench])
        all_projects_opened = all([quest in self.quests for quest in projects])
        all_legends_opened = all([legend in self.legends for legend in legends])

        dpg.configure_item("all_locations", default_value=all_locations_opened)
        dpg.configure_item("all_workbench", default_value=all_workbench_opened)
        dpg.configure_item("all_projects", default_value=all_projects_opened)
        dpg.configure_item("all_legends", default_value=all_legends_opened)

        for quest in locations + workbench + projects:
            dpg.configure_item(quest, default_value=quest in self.quests)
        
        for legend in legends:
            dpg.configure_item(legend, default_value=legend in self.legends)

    def switch_quest(self, _, value, quest):
        if not self.save.is_loaded():
            return

        if value and quest not in self.quests:
            self.quests.append(quest)
            print(f"Opened {quest}")

        if not value and quest in self.quests:
            self.quests.pop(self.quests.index(quest))
            print(f"Closed {quest}")

    def switch_legend(self, _, value, legend):
        if not self.save.is_loaded():
            return

        if not value and legend in self.legends:
            self.legends.remove(legend)

            # Get legend index from list and lock it
            for i, legend_data in enumerate(self.records):
                if legend_data["questId"] == legend:
                    self.records[i]["unlocked"] = False
                    print(f"Locked {legend} legend")
                    return

        if value and legend not in self.legends:
            self.legends.append(legend)

            # Get legend index from list and unlock it
            for i, legend_data in enumerate(self.records):
                if legend_data["questId"] == legend:
                    legend_data["unlocked"] = True
                    break

            else:
                self.records.append({
                    "questId": legend,
                    "unlocked": True
                })

            print(f"Unlocked {legend} legend")

    def switch_all(self, _, value, function_and_fields):
        if not self.save.is_loaded():
            return

        function, fields = function_and_fields

        for field in fields:
            dpg.configure_item(field, default_value=value)
            function(_, value, field)

    def gui(self):
        with dpg.child_window(no_scrollbar=True, border=False):
            with dpg.table(header_row=False, resizable=True):
                dpg.add_table_column()
                dpg.add_table_column()

                with dpg.table_row():
                    with dpg.group():
                        # Locations
                        dpg.add_text(i18n["locations_group"])
                        dpg.add_checkbox(
                            label=i18n["all_locations"],
                            tag="all_locations",
                            callback=self.switch_all,
                            user_data=(self.switch_quest, locations)
                        )

                        for quest in locations:
                            dpg.add_checkbox(
                                label=i18n["locations"][quest],
                                tag=quest,
                                callback=self.switch_quest,
                                user_data=quest
                            )

                        # Workbench
                        dpg.add_text(i18n["workbench_group"])
                        dpg.add_checkbox(
                            label=i18n["all_workbench"],
                            tag="all_workbench",
                            callback=self.switch_all,
                            user_data=(self.switch_quest, workbench)
                        )

                        for quest in workbench:
                            dpg.add_checkbox(
                                label=i18n["workbench"][quest],
                                tag=quest,
                                callback=self.switch_quest,
                                user_data=quest
                            )

                        # Projects
                        dpg.add_text(i18n["projects_group"])
                        dpg.add_checkbox(
                            label=i18n["all_projects"],
                            tag="all_projects",
                            callback=self.switch_all,
                            user_data=(self.switch_quest, projects)
                        )

                        with dpg.group():
                            for project in projects:
                                dpg.add_checkbox(
                                    label=i18n["projects"][project],
                                    tag=project,
                                    callback=self.switch_quest,
                                    user_data=project
                                )

                    with dpg.group():
                        # Legends
                        dpg.add_text(i18n["legends_group"])
                        dpg.add_checkbox(
                            label=i18n["all_legends"],
                            tag="all_legends",
                            callback=self.switch_all,
                            user_data=(self.switch_legend, legends)
                        )

                        with dpg.group():
                            for legend in legends:
                                dpg.add_checkbox(
                                    label=i18n["legends"][legend],
                                    tag=legend,
                                    callback=self.switch_legend,
                                    user_data=legend
                                )
