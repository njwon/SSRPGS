import dearpygui.dearpygui as dpg

available = [
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
    "mutate",
    "automate",
    "fuse_enchantments",
    "break_apart_items",
    "brew_potion",
    "anvil",
]

class ProgressTab:
    def __init__(self, save):
        self.save = save
      
    def load(self):
        pass

    def gui(self):
        dpg.add_text("Открыто")
        for quest in available:
            dpg.add_checkbox(label=quest)