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
        dpg.add_font_chars([0x2666, 0x2248, 0x2605])  # ♦ ≈ ★
        dpg.set_global_font_scale(0.5)
        dpg.bind_font(font)

# Set up values for save editor fields
location_names = (
    "Каменистое плато",
    "Каньон Дедвуд",
    "Пещеры страха",
    "Грибной лес",
    "Призрачные залы",
    "Бурлящая шахта",
    "Ледяной хребет",
    "Храм"
)

location_codes = {
    name: code for name, code in zip(
        location_names,
        (
            "rocky_plateau",
            "deadwood_valley",
            "caustic_caves",
            "fungus_forest",
            "undead_crypt",
            "bronze_mine",
            "icy_ridge",
            "temple"
        )
    )
}

location_name = location_names[0]
location_stars = "1"
location = -1

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

    # For location stats
    dpg.add_int_value(default_value=0, tag="bT")
    dpg.add_double_value(default_value=0.0, tag="aT")
    dpg.add_double_value(default_value=0.0, tag="aHl")
    dpg.add_double_value(default_value=0.0, tag="aHg")
    dpg.add_double_value(default_value=0.0, tag="aKg")
    dpg.add_double_value(default_value=0.0, tag="aRg")

    dpg.add_double_value(default_value=0.0, tag="d")
    dpg.add_double_value(default_value=0.0, tag="Dd")

    dpg.add_double_value(default_value=0.0, tag="DA")
    dpg.add_double_value(default_value=0.0, tag="DF")
    dpg.add_double_value(default_value=0.0, tag="DI")
    dpg.add_double_value(default_value=0.0, tag="DP")
    dpg.add_double_value(default_value=0.0, tag="DV")

# Load values from save
def load_values():
    dpg.set_value("version", save.save_json[save_slot]["version"])
    dpg.set_value("player_name", save.save_json[save_slot]["player_name"])
    dpg.set_value("player_level", save.save_json[save_slot]["player_level"])
    dpg.set_value("player_xp", save.save_json[save_slot]["player_xp"])

    for resource in ("Stone", "Wood", "Tar", "Xi", "Bronze"):
        if resource not in save.save_json[save_slot]["progress_data"]["inventory_data"]:
            save.save_json[save_slot]["progress_data"]["inventory_data"][resource] = 0

        dpg.set_value(resource, save.save_json[save_slot]["progress_data"]["inventory_data"][resource])

    # Get list on opened locations
    for location in save.save_json[save_slot]["progress_data"]["quest_data"]["stats"]:
        # SO... I UNDERSTAND THAT THIS REALIZATION IS WRONG

    change_location(location_name, location_stars)

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

    # Resources
    for resource in ("Stone", "Wood", "Tar", "Xi", "Bronze"):
        save.save_json[save_slot]["progress_data"]["inventory_data"][resource] = dpg.get_value(resource)

    # Location stats for selected location
    for stat in ("bT", "aT", "aHl", "aHg", "aKg", "aRg", "d", "Dd", "DA", "DF", "DI", "DP", "DV"):
        if stat in save.save_json[save_slot]["progress_data"]["quest_data"]["stats"][location]:
            save.save_json[save_slot]["progress_data"]["quest_data"]["stats"][location][stat] = dpg.get_value(stat)

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
        dpg.add_text(message)

def change_save(sender, app_data, user_data):
    global save_slot, location

    save_values()
    save_slot = app_data
    location = -1
    load_values()
    change_location(location_name, location_stars)

def change_location_name(sender, new_location_name):
    change_location(new_location_name, location_stars)

def change_location_stars(sender, new_location_stars):
    change_location(location_name, new_location_stars)

def change_location(new_location_name, new_location_stars):
    global location_name, location_stars, location

    if not save:
        return
    
    # Save old location stats
    if location != -1:
        for stat in ("bT", "aT", "aHl", "aHg", "aKg", "aRg", "d", "Dd", "DA", "DF", "DI", "DP", "DV"):
            if stat in save.save_json[save_slot]["progress_data"]["quest_data"]["stats"][location]:
                save.save_json[save_slot]["progress_data"]["quest_data"]["stats"][location][stat] = dpg.get_value(stat)

    # Determine new location index
    location_name = new_location_name  # Translate name
    location_stars = new_location_stars

    print("name, stars:", new_location_name, new_location_stars)

    # Find location index in array of stats
    new_location_id = location_codes[new_location_name] + (new_location_stars if new_location_stars != "1" else '')
    for i, new_location in enumerate(save.save_json[save_slot]["progress_data"]["quest_data"]["stats"]):
        if new_location["id"] == new_location_id:
            location = i
            break
    else:
        # Location not found
        print(f"Location not found")
        return

    # Change location to another
    for stat in ("bT", "aT", "aHl", "aHg", "aKg", "aRg", "d", "Dd", "DA", "DF", "DI", "DP", "DV"):
        if stat in save.save_json[save_slot]["progress_data"]["quest_data"]["stats"][location]:
            dpg.set_value(stat, save.save_json[save_slot]["progress_data"]["quest_data"]["stats"][location][stat])
        else:
            dpg.set_value(stat, 0)

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
    
    # Header
    with dpg.group(horizontal=True):
        dpg.add_button(label="Открыть", callback=load_file)
        dpg.add_button(label="Сохранить", callback=save_file)

        dpg.add_combo(label="Слот сохранения", width=196, items=[], callback=change_save, tag="save_slots")

    # Tabs
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
            dpg.add_text("Локация")
            dpg.add_combo(label="Название локации", items=location_names, default_value=location_names[0], callback=change_location_name)    
            dpg.add_combo(label="Число звёзд", items=[f"{i}" for i in range(1, 16)], default_value="1", callback=change_location_stars)
            add_help(
                "Уровни локаций для звёзд:\n"
                "★ 1-5    Белый\n"
                "★ 6-10   Бирюзовый\n"
                "★ 11-15  Жёлтый"
            )

            dpg.add_separator()
            dpg.add_text("Время")

            dpg.add_input_int(label="Лучшее время", source="bT")
            add_help("Время отмеряется кадрами:\n30 кадров = 1 секунда")
            dpg.add_input_double(label="Среднее время", source="aT")
            add_help("Время отмеряется кадрами:\n30 кадров = 1 секунда")
            
            dpg.add_separator()
            dpg.add_text("Данные среднего забега")

            dpg.add_input_double(label="Трата оз", source="aHl")
            dpg.add_input_double(label="Пополнение оз", source="aHg")
            dpg.add_input_double(label="Получение Ки", source="aKg")
            dpg.add_input_double(label="Получение ресурса", source="aRg")
            add_help(
                "Для каждй локации свой ресурс:\n"
                "o    Камень     Каменистое плато\n"
                "_/`  Древесина  Каньон Дедвуд\n"
                "≈    Смола      Пещеры страха\n"
                ":.   Бронза     Бурлящая шахта\n"
            )

            dpg.add_separator()
            dpg.add_text("Урон")

            dpg.add_input_double(label="Нанесено урона", source="d")
            dpg.add_input_double(label="Получено урона", source="Dd")

            dpg.add_input_double(label="Нанесено эфиром", source="DA")
            dpg.add_input_double(label="Нанесено огнём", source="DF")
            dpg.add_input_double(label="Нанесено льдом", source="DI")
            dpg.add_input_double(label="Нанесено ядом", source="DP")
            dpg.add_input_double(label="Нанесено энергией", source="DV")

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
