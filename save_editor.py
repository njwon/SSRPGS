# НУ ЭТО ТЫ ЗАГНУЛ С НАЗВАНИЕМ ФАЙЛА
import dearpygui.dearpygui as dpg
from save import Save

# Current save
save = None
save_slot = ""
save_slots = []

dpg.create_context()

with dpg.font_registry():
    default_font = dpg.add_font("mononoki-Regular.ttf", 16)
    dpg.bind_font(default_font)

with dpg.value_registry():
    dpg.add_string_value(default_value="C", tag="player_name")
    dpg.add_int_value(default_value=1.0, tag="player_level")
    # dpg.add_int_value(default_value=0, tag="total_stars")

def load_save_file(sender, app_data):
    global save, save_slots, save_slot

    print(app_data["selections"])

    # Load first file of selected
    for file in app_data["selections"]:
        save = Save(app_data["selections"][file])
        save_slot = f"save_file_{save.save_json["save_file_last_id"]}"

        dpg.configure_item("save_slots", items=save.save_slots, default_value=save_slot)
        break

    dpg.set_value("player_name", save.save_json["save_file_42"]["player_name"])

    # dpg.set_value("player_level", save.save_json["save_file_42"]["player_level"])
    # dpg.set_value("total_stars", save.save_json["save_file_42"]["total_stars"])

def save_save_file():
    global save

    save.save_json["save_file_42"]["player_name"] = dpg.get_value("player_name")
    save.save("primary_save.txt")

with dpg.file_dialog(
    label="Open save file",
    directory_selector=False,
    show=False,
    tag="file_dialog",
    default_path=".", #"/Users/catalyst/Library/Application Support/Martian Rex, Inc_/Stone Story/",
    callback=load_save_file,
    width=600 - 116,
    height=400 - 116
):
    dpg.add_file_extension(".txt")

with dpg.window(tag="Editor"):
    with dpg.tab_bar():
        with dpg.tab(label="Settings"):
            dpg.add_text("About:\nStone Story RPG save editor\nMade by Catalyst\nv 0.0.0")
            dpg.add_separator()

            with dpg.group(horizontal=True):
                dpg.add_button(label="Open save", callback=lambda: dpg.show_item("file_dialog"))
                dpg.add_button(label="Save save", callback=save_save_file)

            dpg.add_combo(label="Save slot", items=[], tag="save_slots")

        with dpg.tab(label="Info"):
            dpg.add_text("info here")
            dpg.add_input_text(label="Player name", source="player_name")
            dpg.add_input_int(label="Player level", source="player_level")
            # dpg.add_input_text(label="Total stars", source="total_stars")

        with dpg.tab(label="Locations"):
            dpg.add_text("locs here")

        with dpg.tab(label="Inventory"):
            dpg.add_text("inv here")
        
        with dpg.tab(label="Quests"):
            dpg.add_text("quests here")

        with dpg.tab(label="Other"):
            dpg.add_text("other here")

        with dpg.tab(label="Json"):
            dpg.add_text("json here")
            
dpg.create_viewport(title="Save editor", width=600, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Editor", True)
dpg.start_dearpygui()
dpg.destroy_context()

# inventory
