import dearpygui.dearpygui as dpg
from natsort import natsorted

from utils import add_help

stats = {
    "time_values": {
        "bT": "Лучшее время",
        "aT": "Среднее время",
    },
    "average_values": {
        "aHl": "Трата оз",
        "aHg": "Пополнение оз",
        "aKg": "Получение Ки",
        "aRg": "Получение ресурса",
    },
    "damage_values": {
        "d": "Нанесено урона",
        "Dd": "Получено урона",
    },
    "element_damage_values": {
        "DA": "Нанесено эфиром",
        "DF": "Нанесено огнём",
        "DI": "Нанесено льдом",
        "DP": "Нанесено ядом",
        "DV": "Нанесено энергией",
    }
}

locations = (
    "rocky_plateau",
    "deadwood_valley",
    "caustic_caves",
    "fungus_forest",
    "undead_crypt",
    "bronze_mine",
    "icy_ridge",
    "temple"
)

class LocationsTab:
    def __init__(self, save):
        self.save = save
        self.location = None
        self.stats = None

    def filter_search(self):
        raise NotImplementedError()

    def load(self):
        self.stats = self.save["progress_data"]["quest_data"]["stats"]

        location_names = natsorted([location["id"] for location in self.save["progress_data"]["quest_data"]["stats"]])
        
        dpg.configure_item("location_names", items=location_names)

        if self.stats:
            dpg.configure_item("stats", show=True)
            self.select_location("load", self.stats[0]["id"])
        else:
            dpg.configure_item("stats", show=False)

    def select_location(self, _, location_name):
        self.location = None
        for location in self.stats:
            if location["id"] == location_name:
                self.location = location
                break
        else:
            print(f"Location {location_name} not found!")
        
        for stat_group in stats:
            for stat in stats[stat_group]:
                if stat in self.location:
                    dpg.configure_item(stat, default_value=self.location[stat])
                else:
                    dpg.configure_item(stat, default_value=0)

    def add_location(self):
        # TODO: Open stats!
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

    def change(self, _, value, stat):
        self.location[stat] = value
        print(f"Changed field: {stat}: {self.location[stat]}")

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
                items=locations,
                default_value=locations[0],
                width=200,
                tag="add_location_name"
            )
            dpg.add_input_int(
                label="Число звёзд",
                min_value=0,
                max_value=15,
                min_clamped=True,
                max_clamped=True,
                width=200,
                tag="add_location_stars"
            )
            dpg.add_checkbox(
                label="Отметить как завершённую",
                tag="add_location_mark_as_visited"
            )

            with dpg.group(horizontal=True):
                dpg.add_button(label="Создать", callback=self.add_location)
                dpg.add_button(
                    label="Отменить",
                    callback=lambda _: dpg.configure_item("add_location", show=False)
                )

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
                dpg.add_listbox(
                    tag="location_names",
                    num_items=12,
                    callback=self.select_location
                )
                dpg.add_button(
                    label="Добавить",
                    callback=lambda _: dpg.configure_item("add_location", show=True)
                )
            
            with dpg.group():
                dpg.add_text("Информация о локации")
                add_help("Время отмеряется кадрами:\n30 кадров = 1 секунда")

                with dpg.child_window(
                    tag="stats",
                    border=False,
                    show=False,
                    no_scrollbar=True
                ):
                    for time_value in stats["time_values"]:
                        dpg.add_input_int(
                            label=stats["time_values"][time_value],
                            tag=time_value,
                            width=200,
                            callback=self.change,
                            user_data=time_value
                        )
                    
                    dpg.add_separator()
                    dpg.add_text("Данные среднего забега")

                    for average_value in stats["average_values"]:
                        dpg.add_input_double(
                            label=stats["average_values"][average_value],
                            tag=average_value,
                            width=200,
                            callback=self.change,
                            user_data=average_value
                        )

                    add_help(
                        "Для каждй локации свой ресурс:\n"
                        "o    Камень     Каменистое плато\n"
                        "_/`  Древесина  Каньон Дедвуд\n"
                        "≈    Смола      Пещеры страха\n"
                        ":.   Бронза     Бурлящая шахта\n"
                    )

                    dpg.add_separator()
                    dpg.add_text("Урон")

                    for damage_value in stats["damage_values"]:
                        dpg.add_input_double(
                            label=stats["damage_values"][damage_value],
                            tag=damage_value,
                            width=200,
                            callback=self.change,
                            user_data=damage_value
                        )
                    
                    dpg.add_separator()
                    dpg.add_text("Стихийный урон")
                    add_help("Влияет на трату стихийных рун при фарме")

                    for element_damage_type in stats["element_damage_values"]:
                        dpg.add_input_double(
                            label=stats["element_damage_values"][element_damage_type],
                            tag=element_damage_type,
                            width=200,
                            callback=self.change,
                            user_data=element_damage_type
                        )
