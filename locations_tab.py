import dearpygui.dearpygui as dpg
from natsort import natsorted

from utils import add_help
from translations import *

stats = {
    "time_values": {
        "bT": "best_time",
        "aT": "average_time",
    },
    "average_values": {
        "aHl": "average_heal_loss",
        "aHg": "average_heal_gain",
        "aKg": "average_ki_gain",
        "aRg": "average_resource_gain",
    },
    "damage_values": {
        "d": "damage_dealt" ,
        "Dd": "damage_devoured",
    },
    "element_damage_values": {
        "DA": "devoured_aether",
        "DF": "devoured_fire",
        "DI": "devoured_ice",
        "DP": "devoured_poison",
        "DV": "devoured_vigor",
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
        self.quest_data = None

        self.location = None

    def load(self):
        self.quest_data = self.save["progress_data"]["quest_data"]
        self.filter_search("load", dpg.get_value("filter_search"))

    def filter_search(self, _, filter_key=""):
        if not self.save.is_loaded():
            return
        
        location_names = natsorted([
            location["id"] for location in self.quest_data["stats"]
            if filter_key in location["id"]
        ])

        if not location_names:        
            dpg.configure_item("location_names", items=location_names)
            dpg.configure_item("stats", show=False)
            
            print("No locations available")
            return
        
        # Select last selected location or first of available
        location_to_select = location_names[0]
        if self.location and self.location["id"] in location_names:
            location_to_select = self.location["id"]

        dpg.configure_item("stats", show=True)
        dpg.configure_item("location_names", items=location_names, default_value=location_to_select)
        self.select_location("load", location_to_select)

    def select_location(self, _, location_name):
        self.location = None
        for location in self.quest_data["stats"]:
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
        dpg.configure_item("add_location", show=False)

        if not self.save.is_loaded():
            return

        location_name = dpg.get_value("add_location_name")
        location_stars = dpg.get_value("add_location_stars")
        is_completed = dpg.get_value("add_location_mark_as_completed")
        
        location = f"{location_name}{location_stars}"
        
        # Exit if location already in stats
        for location_stats in self.quest_data["stats"]:
            if location_stats["id"] == location:
                print(f"Location {location} already exists!")
                dpg.configure_item("location_names", default_value=location)
                self.select_location("add_location", location)
                return

        # Mark star level
        star_levels = self.quest_data["star_levels"]

        if location_name in star_levels:
            if star_levels[location_name] < location_stars:
                star_levels[location_name] = location_stars
        else:
            star_levels[location_name] = location_stars

        print(f"Location {location_name} star level now is {star_levels[location_name]}")

        # Create location
        dpg.configure_item("stats", show=True)
        self.quest_data["stats"].append({
            "id": location,
            "bT": 0,
            "aT": 0,
            "aHl": 0,
            "aHg": 0,
            "aKg": 0
        })
        
        # Check if previous stars completed
        for stars in range(1, location_stars):
            previous_location = f"{location_name}{stars}"

            if location_name not in self.quest_data["has_completed"]:
                self.quest_data["has_completed"].append(location_name)

            if previous_location not in self.quest_data["has_completed"]:
                print(f"Mark as completed {previous_location}")
                if stars >= 3:
                    self.quest_data["stats"].append({
                        "id": previous_location,
                        "bT": 0,
                        "aT": 0,
                        "aHl": 0,
                        "aHg": 0,
                        "aKg": 0
                    })
                self.quest_data["has_completed"].append(previous_location)

        if is_completed:
            self.quest_data["has_completed"].append(location)

        if location_name not in self.quest_data["available"]:
            dpg.configure_item(location_name, default_value=True)
            print(f"New set for {location_name} location created")
            self.quest_data["available"].append(location_name)
            self.quest_data["stats"].append({
                "id": location_name,
                "lpDiff": location_stars,
            })

        # Mark aspiring_stars if location is last
        if location_stars == 15:
            if location_name in self.quest_data["aspiring_star_ids"]:
                i = self.quest_data["aspiring_star_ids"].index(location_name) 
                self.quest_data["aspiring_stars"][i] = str(location_stars + 1)
            else:
                self.quest_data["aspiring_star_ids"].append(location_name)
                self.quest_data["aspiring_stars"].append(str(location_stars + 1))

        # self.load()
        self.filter_search("add_location", "")

        dpg.configure_item("location_names", default_value=location)
        self.select_location("add_location", location)

    def change(self, _, value, stat):
        self.location[stat] = value
        print(f"Changed field: {stat}: {self.location[stat]}")

    def gui(self):
        with dpg.window(
            label=i18n["add_location"],
            pos=((600 - 350) // 2, (400 - 140) // 2),
            width=350,
            height=140,
            show=False,
            tag="add_location"
        ):
            dpg.add_combo(
                label=i18n["location_name"],
                items=locations,
                default_value=locations[0],
                width=200,
                tag="add_location_name"
            )
            dpg.add_input_int(
                label=i18n["location_stars"],
                default_value=3,
                min_value=3,
                max_value=15,
                min_clamped=True,
                max_clamped=True,
                width=200,
                tag="add_location_stars"
            )
            dpg.add_checkbox(
                label=i18n["mark_location_as_completed"],
                tag="add_location_mark_as_completed"
            )

            with dpg.group(horizontal=True):
                dpg.add_button(label=i18n["create"], callback=self.add_location)
                dpg.add_button(
                    label=i18n["cancel"],
                    callback=lambda _: dpg.configure_item("add_location", show=False)
                )

        with dpg.group(horizontal=True):
            with dpg.group(width=175):
                dpg.add_text(i18n["visited_locations"])
                add_help(i18n["locations_list_info"])

                dpg.add_input_text(
                    hint=i18n["search"],
                    tag="filter_search",
                    callback=self.filter_search
                )
                dpg.add_listbox(
                    tag="location_names",
                    num_items=12,
                    callback=self.select_location
                )
                dpg.add_button(
                    label=i18n["add"],
                    callback=lambda _: dpg.configure_item("add_location", show=True)
                )
            
            with dpg.group():
                dpg.add_text(i18n["location_information"])
                add_help(i18n["time_measured_in_frames_info"])

                with dpg.child_window(
                    tag="stats",
                    border=False,
                    show=False,
                    no_scrollbar=True
                ):
                    for time_value in stats["time_values"]:
                        dpg.add_input_int(
                            label=i18n["location_stats"][stats["time_values"][time_value]],
                            tag=time_value,
                            width=200,
                            callback=self.change,
                            user_data=time_value
                        )
                    
                    dpg.add_separator()
                    dpg.add_text(i18n["average_run_data"])

                    for average_value in stats["average_values"]:
                        dpg.add_input_double(
                            label=i18n["location_stats"][stats["average_values"][average_value]],
                            tag=average_value,
                            width=200,
                            callback=self.change,
                            user_data=average_value
                        )

                    add_help(i18n["location_resources_info"])

                    dpg.add_separator()
                    dpg.add_text(i18n["damage"])

                    for damage_value in stats["damage_values"]:
                        dpg.add_input_double(
                            label=i18n["location_stats"][stats["damage_values"][damage_value]],
                            tag=damage_value,
                            width=200,
                            callback=self.change,
                            user_data=damage_value
                        )
                    
                    dpg.add_separator()
                    dpg.add_text(i18n["damage"])
                    add_help(i18n["element_damage_affect_on_rune_info"])

                    for element_damage_type in stats["element_damage_values"]:
                        dpg.add_input_double(
                            label=i18n["location_stats"][stats["element_damage_values"][element_damage_type]],
                            tag=element_damage_type,
                            width=200,
                            callback=self.change,
                            user_data=element_damage_type
                        )
