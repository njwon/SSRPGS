import dearpygui.dearpygui as dpg

available_locations = {
    "temple": "Храм",
    "cross_bridge": "Переход по посту",
    "icy_ridge": "Ледяной хребет",
    "bronze_gate": "Бронзовые врата",
    "bronze_mine": "Бурлящая шахта",
    "cross_deadwood_river": "Переплыть реку Дедвуд",
    "undead_crypt": "Призрачные залы",
    "undead_crypt_intro": "Призрачные врата",
    "uulaa_shop": 'Лавка "Горячий ключ"',
    "mushroom_shop": "Грибная лавка",
    "fungus_forest": "Грибной лес",
    "waterfall": "Водопад Дедвуд",
    "caustic_caves": "Пещеры страха",
    "deadwood_valley": "Каньон Дедвуд",
    "rocky_plateau": "Каменистое плато",
}

available_workbench = {
    "mutate": "Изменить",
    "automate": "Автоматизировать",
    "fuse_enchantments": "Выковать чары",
    "break_apart_items": "Сломать предметы",
    "brew_potion": "Сварить зелье",
    "anvil": "Улучшить предметы",
}

# TODO: Realize wtf if should be there
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

all_quests = list(available_locations | available_workbench)

class ProgressTab:
    def __init__(self, save):
        self.save = save
        self.quests = None

    def load(self):
        self.quests = self.save["progress_data"]["quest_data"]["available"]
        
        all_locations_opened = all([quest in self.quests for quest in available_locations])
        all_workbench_opened = all([quest in self.quests for quest in available_workbench])

        dpg.configure_item("all_locations", default_value=all_locations_opened)
        dpg.configure_item("all_workbench", default_value=all_workbench_opened)
        
        for quest in all_quests:
            dpg.configure_item(quest, default_value=quest in self.quests)
    
    def switch(self, _, value, quest):
        if not self.save.is_loaded():
            return

        if value and quest not in self.quests:
            self.quests.append(quest)
            print(f"Opened {quest}")
        
        if not value and quest in self.quests:
            self.quests.pop(self.quests.index(quest))
            print(f"Closed {quest}")
    
    def switch_all(self, _, value, quests):
        if not self.save.is_loaded():
            return

        for quest in quests:
            dpg.configure_item(quest, default_value=value)
            self.switch(_, value, quest)
        
    def gui(self):
        with dpg.child_window(no_scrollbar=True, border=False):
            with dpg.table(header_row=False):
                dpg.add_table_column()
                dpg.add_table_column()

                with dpg.table_row():
                    with dpg.group():
                        dpg.add_text("Локации")
                        dpg.add_checkbox(
                            label="Все локации",
                            tag="all_locations",
                            callback=self.switch_all,
                            user_data=available_locations
                        )

                        for quest in available_locations:
                            dpg.add_checkbox(
                                label=available_locations[quest],
                                tag=quest,
                                callback=self.switch,
                                user_data=quest
                            )

                    with dpg.group():
                        dpg.add_text("Верстак")
                        dpg.add_checkbox(
                            label="Все утилиты",
                            tag="all_workbench",
                            callback=self.switch_all,
                            user_data=available_workbench
                        )

                        for quest in available_workbench:
                            dpg.add_checkbox(
                                label=available_workbench[quest],
                                tag=quest,
                                callback=self.switch,
                                user_data=quest
                            )
