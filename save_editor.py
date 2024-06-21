import dearpygui.dearpygui as dpg
from subprocess import check_output
from natsort import natsorted
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
        dpg.add_font_chars([ord(c) for c in "♦≈★"])
        dpg.set_global_font_scale(0.5)
        dpg.bind_font(font)

# Set up values for save editor fields
locations = {}
location_names = ()
selected_location_index = -1

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

class InventoryItem():
    def __init__(self, index, data):
        self.index = index
        self.data = data

    def __repr__(self):
        return self.data["id"]
    
    def get_data(self):
        return self.data

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

    load_locations()

    # Inventory
    inventory_item_names = [InventoryItem(i, item) for i, item in enumerate(save.save_json[save_slot]["progress_data"]["inventory_data"]["itms"])]
    dpg.configure_item("inventory", items=inventory_item_names)

def load_locations(default_location=None):
    global location_names

    # Set list of locations
    print(save_slot)
    location_names = natsorted([location["id"] for location in save.save_json[save_slot]["progress_data"]["quest_data"]["stats"]])
    dpg.configure_item("location_names", items=location_names)

    # Select first location in locations
    if location_names:
        dpg.configure_item("stats", show=True)
        dpg.configure_item("location_names", default_value=default_location if default_location else location_names[0])
        select_location(None, default_location if default_location else location_names[0])
    else:
        dpg.configure_item("stats", show=False)

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
    if selected_location_index != -1:
        for stat in ("bT", "aT", "aHl", "aHg", "aKg", "aRg", "d", "Dd", "DA", "DF", "DI", "DP", "DV"):
            if stat in save.save_json[save_slot]["progress_data"]["quest_data"]["stats"][selected_location_index] or dpg.get_value(stat):
                save.save_json[save_slot]["progress_data"]["quest_data"]["stats"][selected_location_index][stat] = dpg.get_value(stat)

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

def change_save(sender, new_save_slot):
    global save_slot, selected_location_index

    save_values()
    save_slot = new_save_slot
    selected_location_index = -1
    load_values()

def select_location(sender, location_name):
    global selected_location_index
    
    # Save old location stats
    if selected_location_index != -1:
        for stat in ("bT", "aT", "aHl", "aHg", "aKg", "aRg", "d", "Dd", "DA", "DF", "DI", "DP", "DV"):
            if stat in save.save_json[save_slot]["progress_data"]["quest_data"]["stats"][selected_location_index] or dpg.get_value(stat):
                save.save_json[save_slot]["progress_data"]["quest_data"]["stats"][selected_location_index][stat] = dpg.get_value(stat)

    # Get index because stats is an array
    selected_location_index = -1
    for i, location in enumerate(save.save_json[save_slot]["progress_data"]["quest_data"]["stats"]):
        if location["id"] == location_name:
            selected_location_index = i
            break
    else:
        print("Location not found!")
        return

    for stat in ("bT", "aT", "aHl", "aHg", "aKg", "aRg", "d", "Dd", "DA", "DF", "DI", "DP", "DV"):
        if stat in save.save_json[save_slot]["progress_data"]["quest_data"]["stats"][selected_location_index]:
            dpg.set_value(stat, save.save_json[save_slot]["progress_data"]["quest_data"]["stats"][selected_location_index][stat])
        else:
            dpg.set_value(stat, 0)

def filter_items(sender, filter):
    if not save:
        return
    
    inventory_item_names = [InventoryItem(i, item) for i, item in enumerate(save.save_json[save_slot]["progress_data"]["inventory_data"]["itms"]) if filter in item["id"]]
    dpg.configure_item("inventory", items=inventory_item_names)

def add_location():
    if not save:
        return
    
    location_name = dpg.get_value("add_location_name")
    location_stars = dpg.get_value("add_location_stars")
    mark_as_visited = dpg.get_value("add_location_mark_as_visited")
    
    location = f"{location_name}{location_stars if location_stars else ''}"

    for location_stats in save.save_json[save_slot]["progress_data"]["quest_data"]["stats"]:
        if location_stats["id"] == location:
            break
    else:
        # Location not in stats
        save.save_json[save_slot]["progress_data"]["quest_data"]["stats"].append({
            "id": location,
            "bT": 0,
            "aT": 0,
            "aHl": 0,
            "aHg": 0,
            "aKg": 0
        })

        if mark_as_visited:
            save.save_json[save_slot]["progress_data"]["quest_data"]["has_completed"].append(location)

        # Mark star level
        if location in save.save_json[save_slot]["progress_data"]["quest_data"]["star_levels"]:
            if save.save_json[save_slot]["progress_data"]["quest_data"]["star_levels"][location_name] < location_stars:
                save.save_json[save_slot]["progress_data"]["quest_data"]["star_levels"][location_name] = location_stars
        else:
            save.save_json[save_slot]["progress_data"]["quest_data"]["star_levels"][location] = location_stars

        # Mark location if new one
        if location_name not in save.save_json[save_slot]["progress_data"]["quest_data"]["available"]:
            save.save_json[save_slot]["progress_data"]["quest_data"]["available"].append(location_name)
        else:
            # New set of locations
            save.save_json[save_slot]["progress_data"]["quest_data"]["stats"].append({
                "id": location_name,
                "lpDiff": location_stars,
                "bT": 0,
                "aT": 0,
                "aHl": 0,
                "aHg": 0,
                "aKg": 0,
            })

        # Mark aspiring_stars if location is last
        if location_stars == 15:
            if location_name in save.save_json[save_slot]["progress_data"]["quest_data"]["aspiring_star_ids"]:
                i = save.save_json[save_slot]["progress_data"]["quest_data"]["aspiring_star_ids"].index(location_name) 
                
                save.save_json[save_slot]["progress_data"]["quest_data"]["aspiring_stars"][i] = str(location_stars)
            else:
                save.save_json[save_slot]["progress_data"]["quest_data"]["aspiring_star_ids"].append(location_name)
                save.save_json[save_slot]["progress_data"]["quest_data"]["aspiring_stars"].append(str(location_stars))

        # Update locations list
        load_locations(location)

    dpg.configure_item("add_location", show=False)

def open_item(sender, item):
    # Save data
    # ...

    dpg.delete_item("item_settings", children_only=True)
    
    # Recursevly parse all item setting dict
    dpg.add_text(f"Item: {item}", parent="item_settings")
    dpg.add_input_int(parent="item_settings", label=item, width=200)
    print(item, type(item))

def save_json():
    if save:
        save.save_as_json("formatted.json")
        print("exported json")

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
    with dpg.tab_bar():
        with dpg.tab(label="Настройки"):
            dpg.add_text("Stone Story RPG save editor\nv 0.0.0")

            dpg.add_button(label="Экспортировать JSON", callback=save_json)

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
                with dpg.group(width=175):
                    dpg.add_text("Посещённые локации")
                    add_help(
                        "Имена локаций:\n"
                        "rocky_plateau    Каменистое плато\n"
                        "deadwood_valley  Каньон Дедвуд\n"
                        "caustic_caves    Пещеры страха\n"
                        "fungus_forest    Грибной лес\n"
                        "undead_crypt     Призрачные залы\n"
                        "bronze_mine      Бурлящая шахта\n"
                        "icy_ridge        Ледяной хребет\n"
                        "temple           Храм\n\n"
                        "Уровни:\n"
                        "★ 1-5    Белый\n"
                        "★ 6-10   Бирюзовый\n"
                        "★ 11-15  Жёлтый\n"
                    )

                    dpg.add_listbox(tag="location_names", num_items=14, callback=select_location)
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Добавить", callback=lambda _: dpg.configure_item("add_location", show=True))

                    with dpg.window(
                        label="Добавить локацию",
                        pos=((600 - 350) // 2, (400 - 140) // 2),
                        width=350,
                        height=140,
                        show=False,
                        tag="add_location"
                    ):
                        dpg.add_combo(
                            label="Название локации",
                            items=["rocky_plateau", "deadwood_valley", "caustic_caves", "fungus_forest", "undead_crypt", "bronze_mine", "icy_ridge", "temple"],
                            default_value="rocky_plateau",
                            width=200,
                            tag="add_location_name"
                        )
                        dpg.add_input_int(label="Число звёзд", min_value=0, max_value=15, min_clamped=True, max_clamped=True, width=200, tag="add_location_stars")
                        dpg.add_checkbox(label="Отметить как завершённую", tag="add_location_mark_as_visited")

                        with dpg.group(horizontal=True):
                            dpg.add_button(label="Создать", callback=add_location)
                            dpg.add_button(label="Отменить", callback=lambda _: dpg.configure_item("add_location", show=False))
                
                with dpg.group():
                    dpg.add_text("Информация о локации")
                    
                    with dpg.child_window(tag="stats", border=False, show=False, no_scrollbar=True):
                        dpg.add_input_int(label="Лучшее время", width=200, source="bT")
                        add_help("Время отмеряется кадрами:\n30 кадров = 1 секунда")
                        dpg.add_input_double(label="Среднее время", width=200, source="aT")
                        add_help("Время отмеряется кадрами:\n30 кадров = 1 секунда")
                        
                        dpg.add_separator()
                        dpg.add_text("Данные среднего забега")

                        dpg.add_input_double(label="Трата оз", width=200, source="aHl")
                        dpg.add_input_double(label="Пополнение оз", width=200, source="aHg")
                        dpg.add_input_double(label="Получение Ки", width=200, source="aKg")
                        dpg.add_input_double(label="Получение ресурса", width=200, source="aRg")
                        add_help(
                            "Для каждй локации свой ресурс:\n"
                            "o    Камень     Каменистое плато\n"
                            "_/`  Древесина  Каньон Дедвуд\n"
                            "≈    Смола      Пещеры страха\n"
                            ":.   Бронза     Бурлящая шахта\n"
                        )

                        dpg.add_separator()
                        dpg.add_text("Урон")

                        dpg.add_input_double(label="Нанесено урона", width=200, source="d")
                        dpg.add_input_double(label="Получено урона", width=200, source="Dd")
                        
                        dpg.add_separator()
                        dpg.add_text("Стихийный урон")
                        add_help("Влияет на трату стихийных рун при фарме")

                        dpg.add_input_double(label="Нанесено эфиром", width=200, source="DA")
                        dpg.add_input_double(label="Нанесено огнём", width=200, source="DF")
                        dpg.add_input_double(label="Нанесено льдом", width=200, source="DI")
                        dpg.add_input_double(label="Нанесено ядом", width=200, source="DP")
                        dpg.add_input_double(label="Нанесено энергией", width=200, source="DV")

        with dpg.tab(label="Инвентарь"):
            with dpg.group(horizontal=True):
                with dpg.group(width=175):
                    dpg.add_text("Предметы")
                    dpg.add_input_text(callback=filter_items)
                    dpg.add_listbox(tag="inventory", num_items=12, callback=open_item)
                    dpg.add_button(label="Создать предмет")

                with dpg.group():
                    dpg.add_text("Данные предмета", tag="item_info")

                    dpg.add_group(tag="item_settings")  # conrainer for item setting

        with dpg.tab(label="Квесты"):
            pass

        with dpg.tab(label="Таймеры"):
            pass

        with dpg.tab(label="JSON"):
            pass

        with dpg.tab(label="Статистика"):
            pass
            
dpg.create_viewport(title="Редактор сохранений Stone Story RPG", width=600, height=412)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Editor", True)
dpg.start_dearpygui()
dpg.destroy_context()
