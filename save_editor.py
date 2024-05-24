# НУ ЭТО ТЫ ЗАГНУЛ С НАЗВАНИЕМ ФАЙЛА
import dearpygui.dearpygui as dpg
from save import Save

# Current save
save = None
save_slot = ""
save_slots = []

dpg.create_context()

with dpg.font_registry():
    with dpg.font("mononoki-Regular.ttf", 32) as font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        dpg.set_global_font_scale(0.5)
        dpg.bind_font(font)

with dpg.value_registry():
    dpg.add_string_value(default_value="", tag="version")
    dpg.add_string_value(default_value="", tag="player_name")
    dpg.add_int_value(default_value=0, tag="player_level")
    dpg.add_int_value(default_value=0, tag="player_xp")

def load():
    dpg.set_value("version", save.save_json[save_slot]["version"])
    dpg.set_value("player_name", save.save_json[save_slot]["player_name"])
    dpg.set_value("player_level", save.save_json[save_slot]["player_level"])
    dpg.set_value("player_xp", save.save_json[save_slot]["player_xp"])

def data_save():
    save.save_json[save_slot]["version"] = dpg.get_value("version")
    save.save_json[save_slot]["progress_data"]["version"] = dpg.get_value("version")
    save.save_json[save_slot]["player_name"] = dpg.get_value("player_name")
    save.save_json[save_slot]["progress_data"]["hero_settings"]["playerName"] = dpg.get_value("player_name")
    save.save_json[save_slot]["player_level"] = dpg.get_value("player_level")
    save.save_json[save_slot]["progress_data"]["xp"]["currentLevel"] = dpg.get_value("player_level")
    save.save_json[save_slot]["player_xp"] = dpg.get_value("player_xp")
    save.save_json[save_slot]["progress_data"]["xp"]["currentXP"] = dpg.get_value("player_xp")

def load_save_file(sender, app_data):
    global save, save_slots, save_slot

    dpg.configure_item("loading", show=True)
    print(app_data["selections"])

    # Load first file of selected
    for file in app_data["selections"]:
        save = Save(app_data["selections"][file])
        save_slot = f"save_file_{save.save_json["save_file_last_id"]}"

        dpg.configure_item("save_slots", items=save.save_slots, default_value=save_slot)
        break

    load()
    dpg.configure_item("loading", show=False)

def save_save_file():
    global save
    if not save_slot:
        return
    
    dpg.configure_item("loading", show=True)
    print("going to save file")
    data_save()
    save.save("primary_save.txt")
    print("file saved")
    dpg.configure_item("loading", show=False)

with dpg.file_dialog(
    label="Открыть файл сохранения",
    directory_selector=False,
    show=False,
    tag="file_dialog",
    default_path=".", #"/Users/catalyst/Library/Application Support/Martian Rex, Inc_/Stone Story/",
    callback=load_save_file,
    width=600 - 116,
    height=400 - 116
):
    dpg.add_file_extension(".txt")

def add_help(message):
    last_item = dpg.last_item()
    group = dpg.add_group(horizontal=True)

    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))
    t = dpg.add_text("(?)", color=[0, 255, 0])

    with dpg.tooltip(t):
        dpg.add_text(message)

def log(sender, app_data, user_data):
    print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")

def change_save(sender, app_data, user_data):
    global save, save_slot
    save_slot = app_data
    load()

with dpg.window(tag="Editor"):
    with dpg.group(horizontal=True):
        dpg.add_button(label="Открыть", callback=lambda: dpg.show_item("file_dialog"))
        # check out simple module for details
        dpg.add_button(label="Сохранить", callback=save_save_file)
        with dpg.window(show=False, modal=True, no_title_bar=True, no_resize=True, tag="loading", popup=True, pos=[(600 - 64) // 2,
            (400 - 64) // 2], width=64, height=64, min_size=[32, 32]):
            # dpg.add_text("Запись файла")
            dpg.add_loading_indicator(circle_count=8)

        dpg.add_combo(label="Слот сохранения", width=196, items=[], callback=change_save, tag="save_slots")

    with dpg.tab_bar(track_offset=1):
        with dpg.tab(label="Настройки"):
            dpg.add_text("Stone Story RPG save editor\nv 0.0.0")

        with dpg.tab(label="Общее"):
            dpg.add_input_text(label="Версия сохранения", source="version")
            dpg.add_input_text(label="Имя персонажа", source="player_name")
            dpg.add_input_int(label="Уровень персонажа", source="player_level")
            add_help("Влияет на максимальное оффлайн время по формуле:\nmax_chests = 120 + 6 * player_level")
            dpg.add_input_int(label="Очки опыта", source="player_xp")

        with dpg.tab(label="Локации"):
            pass

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
            
dpg.create_viewport(title="Редактор сохранений Stone Story RPG", width=600, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Editor", True)
dpg.start_dearpygui()
dpg.destroy_context()
