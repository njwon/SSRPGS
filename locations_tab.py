import dearpygui.dearpygui as dpg
from natsort import natsorted

from utils import add_help

class LocationsTab:
    def __init__(self, save):
        self.save = save
        self.selected_location_index = None
        self.init_registry()

    def filter_search(self):
        raise NotImplementedError()

    def init_registry(self):
        with dpg.value_registry():
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

    def dump(self):
        if self.selected_location_index is None:
            return
        
        for stat in ("bT", "aT", "aHl", "aHg", "aKg", "aRg", "d", "Dd", "DA", "DF", "DI", "DP", "DV"):
            if stat in self.save["progress_data"]["quest_data"]["stats"][self.selected_location_index] or dpg.get_value(stat):
                self.save["progress_data"]["quest_data"]["stats"][self.selected_location_index][stat] = dpg.get_value(stat)

    def load(self, default_location=None):
        # Set list of locations
        location_names = natsorted([location["id"] for location in self.save["progress_data"]["quest_data"]["stats"]])
        dpg.configure_item("location_names", items=location_names)

        # Select first location in locations
        if location_names:
            dpg.configure_item("stats", show=True)
            
            if default_location is None:
                default_location = location_names[0]

            dpg.configure_item("location_names", default_value=default_location)
            self.select_location("load", default_location)
        else:
            self.selected_location_index = None
            dpg.configure_item("stats", show=False)

    def select_location(self, _, location_name):
        # Dump old location
        self.dump()

        # Get index because stats is an array
        self.selected_location_index = None
        
        for i, location in enumerate(self.save["progress_data"]["quest_data"]["stats"]):
            if location["id"] == location_name:
                self.selected_location_index = i
                break

        for stat in ("bT", "aT", "aHl", "aHg", "aKg", "aRg", "d", "Dd", "DA", "DF", "DI", "DP", "DV"):
            if stat in self.save["progress_data"]["quest_data"]["stats"][self.selected_location_index]:
                dpg.set_value(stat, self.save["progress_data"]["quest_data"]["stats"][self.selected_location_index][stat])
            else:
                dpg.set_value(stat, 0)

    def add_location(self):
        dpg.configure_item("add_location", show=False)

        if not self.save.is_loaded():
            return
        
        location_name = dpg.get_value("add_location_name")
        location_stars = dpg.get_value("add_location_stars")
        mark_as_visited = dpg.get_value("add_location_mark_as_visited")
        
        location = f"{location_name}{location_stars if location_stars else ''}"

        # Mark star level
        if location_name in self.save["progress_data"]["quest_data"]["star_levels"]:
            if self.save["progress_data"]["quest_data"]["star_levels"][location_name] < location_stars:
                self.save["progress_data"]["quest_data"]["star_levels"][location_name] = location_stars
        else:
            self.save["progress_data"]["quest_data"]["star_levels"][location] = location_stars

        # Exit if location exists
        for location_stats in self.save["progress_data"]["quest_data"]["stats"]:
            if location_stats["id"] == location:
                return
    
        # Location not in stats
        self.save["progress_data"]["quest_data"]["stats"].append({
            "id": location,
            "bT": 0,
            "aT": 0,
            "aHl": 0,
            "aHg": 0,
            "aKg": 0
        })

        if mark_as_visited:
            self.save["progress_data"]["quest_data"]["has_completed"].append(location)

        # Open location in quests tab
        if location_name not in self.save["progress_data"]["quest_data"]["available"]:
            self.save["progress_data"]["quest_data"]["available"].append(location_name)

        # Mark location if new one
        if location_name not in self.save["progress_data"]["quest_data"]["available"]:
            self.save["progress_data"]["quest_data"]["available"].append(location_name)
            self.save["progress_data"]["quest_data"]["stats"].append({
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
            if location_name in self.save["progress_data"]["quest_data"]["aspiring_star_ids"]:
                i = self.save["progress_data"]["quest_data"]["aspiring_star_ids"].index(location_name) 
                
                self.save["progress_data"]["quest_data"]["aspiring_stars"][i] = str(location_stars)
            else:
                self.save["progress_data"]["quest_data"]["aspiring_star_ids"].append(location_name)
                self.save["progress_data"]["quest_data"]["aspiring_stars"].append(str(location_stars))

        # Update locations list
        self.load(default_location=location)

    def gui(self):
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
                dpg.add_button(label="Создать", callback=self.add_location)
                dpg.add_button(label="Отменить", callback=lambda _: dpg.configure_item("add_location", show=False))

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

                dpg.add_input_text(hint="Поиск", callback=self.filter_search)
                dpg.add_listbox(tag="location_names", num_items=12, callback=self.select_location)
                dpg.add_button(label="Добавить", callback=lambda _: dpg.configure_item("add_location", show=True))
            
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
