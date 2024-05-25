import dearpygui.dearpygui as dpg
from subprocess import check_output
from sys import executable
from save import Save

# Current save
save = None
save_slot = ""
save_slots = []

dpg.create_context()

# Set up font
with dpg.font_registry():
    with dpg.font("mononoki-Regular.ttf", 32) as font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        dpg.add_font_chars([0x2666, 0x2248])
        dpg.set_global_font_scale(0.5)
        dpg.bind_font(font)

# Set up values for save editor fields
locations = {}
location_names = ()

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

# Load values from save
def load_values():
    global location_names

    dpg.set_value("version", save.save_json[save_slot]["version"])
    dpg.set_value("player_name", save.save_json[save_slot]["player_name"])
    dpg.set_value("player_level", save.save_json[save_slot]["player_level"])
    dpg.set_value("player_xp", save.save_json[save_slot]["player_xp"])

    for resource in ("Stone", "Wood", "Tar", "Xi", "Bronze"):
        if resource not in save.save_json[save_slot]["progress_data"]["inventory_data"]:
            save.save_json[save_slot]["progress_data"]["inventory_data"][resource] = 0

        dpg.set_value(resource, save.save_json[save_slot]["progress_data"]["inventory_data"][resource])

    location_names = sorted([location["id"] for location in save.save_json[save_slot]["progress_data"]["quest_data"]["stats"]])
    # set locs list
    dpg.configure_item("location_names", items=location_names)

# Store values to save
def save_values():
    global locations

    save.save_json[save_slot]["version"] = dpg.get_value("version")
    save.save_json[save_slot]["progress_data"]["version"] = dpg.get_value("version")

    save.save_json[save_slot]["player_name"] = dpg.get_value("player_name")
    save.save_json[save_slot]["progress_data"]["hero_settings"]["playerName"] = dpg.get_value("player_name")

    save.save_json[save_slot]["player_level"] = dpg.get_value("player_level")
    save.save_json[save_slot]["progress_data"]["xp"]["currentLevel"] = dpg.get_value("player_level")

    save.save_json[save_slot]["player_xp"] = dpg.get_value("player_xp")
    save.save_json[save_slot]["progress_data"]["xp"]["currentXP"] = dpg.get_value("player_xp")

    for resource in ("Stone", "Wood", "Tar", "Xi", "Bronze"):
        save.save_json[save_slot]["progress_data"]["inventory_data"][resource] = dpg.get_value(resource)

def load_file():
    global save, save_slot
    save_file = check_output([executable, "get_file.py"])  # I don't know what's wrong with dpg

    if not save_file:
        return

    dpg.configure_item("loading", show=True) # Show loading

    save = Save(save_file)
    save_slot = f"save_file_{save.save_json["save_file_last_id"]}"
    dpg.configure_item("save_slots", items=save.save_slots, default_value=save_slot)
    load_values()

    dpg.configure_item("loading", show=False) # Done loading

def save_file():
    if not save_slot:
        return
    
    dpg.configure_item("loading", show=True)

    save_values()
    save.save("primary_save.txt")
    
    dpg.configure_item("loading", show=False)
    
    print("file saved")

# Green (?) block, on hover returns popup
def add_help(message):
    last_item = dpg.last_item()
    group = dpg.add_group(horizontal=True)

    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))

    with dpg.tooltip(dpg.add_text("(?)", color=[0, 255, 0])):
        print(dpg.mvThemeCol_ButtonActive)
        dpg.add_text(message)

def change_save(sender, app_data, user_data):
    global save_slot

    save_values()
    save_slot = app_data
    load_values()

# GUI
with dpg.window(tag="Editor"):
    # Loading window
    with dpg.window(
        show=False,
        modal=True,
        no_title_bar=True,
        no_resize=True,
        no_move=True,
        tag="loading",
        pos=[(600 - 64) // 2, (400 - 64) // 2],
        width=64,
        height=64,
        min_size=[32, 32]
    ):
        dpg.add_loading_indicator(circle_count=8)
    
    with dpg.group(horizontal=True):
        dpg.add_button(label="Открыть", callback=load_file)
        dpg.add_button(label="Сохранить", callback=save_file)

        dpg.add_combo(label="Слот сохранения", width=196, items=[], callback=change_save, tag="save_slots")

    with dpg.tab_bar(track_offset=1):
        with dpg.tab(label="Настройки"):
            dpg.add_text("Stone Story RPG save editor\nv 0.0.0")

        with dpg.tab(label="Общее"):
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

        with dpg.tab(label="Локации"):
            with dpg.group(horizontal=True):
                with dpg.group(width=200):
                    dpg.add_text("Посещённые локации")
                    dpg.add_listbox(location_names, tag="location_names", num_items=15)
                    
                with dpg.group(width=250):
                    dpg.add_text("Информация о локации")
                    dpg.add_input_int(label="some value")
                    dpg.add_text("locatoin info")
                    dpg.add_text("locatoin info")
                    dpg.add_text("locatoin info")

        with dpg.tab(label="Инвентарь"):
            pass
        
        with dpg.tab(label="Квесты"):
            pass

        with dpg.tab(label="Таймеры"):
            pass

        with dpg.tab(label="JSON"):
            pass

        with dpg.tab(label="Статистика"):
            pass
            
dpg.create_viewport(title="Редактор сохранений Stone Story RPG", width=600, height=406)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Editor", True)
dpg.start_dearpygui()
dpg.destroy_context()
