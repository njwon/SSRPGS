import dearpygui.dearpygui as dpg
from natsort import natsorted

from tools.setup import *
from tools.utils import add_help

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
        self.star_levels = None

        self.location = None

    def load(self):
        self.quest_data = self.save["progress_data"]["quest_data"]
        self.star_levels = self.save["progress_data"]["quest_data"]["star_levels"]
        self.filter_search("load", dpg.get_value("location_filter"))

    def filter_search(self, _, filter_key=""):
        if not self.save.is_loaded():
            return
        
        # Get available locations by star level
        location_names = []

        for location in self.star_levels:
            for star_level in range(3, self.star_levels[location] + 1):
                location_names.append(f"{location}{star_level}")
        
        location_names = natsorted([
            location for location in location_names
            if filter_key in location
        ])

        if not location_names:
            dpg.configure_item("location_names", items=location_names)
            dpg.configure_item("stats", show=False)
            
            print("No locations available")
            return

        # Select location for combo
        last_selected_location = dpg.get_value("location_names")
        if last_selected_location in location_names:
            location_to_select = last_selected_location
        else:
            location_to_select = location_names[0]

        dpg.configure_item(
            "location_names",
            items=location_names,
            default_value=location_to_select
        )
        dpg.configure_item(
            "stats",
            show=True
        )
        self.select_location(
            "load",
            location_to_select
        )

    def select_location(self, _, location_name):
        self.location = None

        # Get location from list
        for location in self.quest_data["stats"]:
            if location["id"] == location_name:
                self.location = location
                break

        # Load stats to fields
        for stat_group in stats:
            for stat in stats[stat_group]:
                if self.location and stat in self.location:
                    dpg.configure_item(stat, default_value=self.location[stat])
                else:
                    dpg.configure_item(stat, default_value=0)

    def add_location(self):
        dpg.configure_item("add_location", show=False)
 
        if not self.save.is_loaded():
            return

        location_name = dpg.get_value("add_location_name")
        location_stars = dpg.get_value("add_location_stars")

        location = f"{location_name}{location_stars}"

        # Open location by star level
        if location_name in self.star_levels:
            if self.star_levels[location_name] < location_stars:
                self.star_levels[location_name] = location_stars
            else:
                print(f"Location {location} already exists!")
        else:
            self.star_levels[location_name] = location_stars

        # Check location availability
        if location_name not in self.quest_data["available"]:
            dpg.configure_item(  # Call to progress tab
                location_name,
                default_value=True
            )

            self.quest_data["available"].append(location_name)
            print(f"Marked location {location_name} as available")

        # Clear filter and open new location
        dpg.configure_item("location_names", default_value=location)
        dpg.configure_item("location_filter", default_value="")

        self.filter_search("add_location", "")
        self.select_location("add_location", location)

    def change(self, _, value, stat):
        if not self.location:
            self.location = {"id": dpg.get_value("location_names")}
            self.quest_data["stats"].append(self.location)

            print(f"Created stats for location {self.location["id"]}")

        self.location[stat] = value
        print(f"Changed field: {stat}: {self.location[stat]}")

    def gui(self):
        # Add location window
        with dpg.window(
            label=i18n["add_location"],
            pos=((WIDTH - 350) // 2 * SCALE, (HEIGHT - 112) // 2 * SCALE),
            width=350 * SCALE,
            height=112 * SCALE,
            show=False,
            tag="add_location"
        ):
            dpg.add_combo(
                label=i18n["location_name"],
                items=locations,
                default_value=locations[0],
                width=200 * SCALE,
                tag="add_location_name"
            )
            dpg.add_input_int(
                label=i18n["location_stars"],
                default_value=3,
                min_value=3,
                min_clamped=True,
                width=200 * SCALE,
                tag="add_location_stars"
            )
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label=i18n["create"],
                    callback=self.add_location
                )
                dpg.add_button(
                    label=i18n["cancel"],
                    callback=lambda _: dpg.configure_item(
                        "add_location",
                        show=False
                    )
                )

        with dpg.child_window(border=False, no_scrollbar=True):
            with dpg.group(horizontal=True):
                # List of available locations
                with dpg.group(width=175 * SCALE):
                    dpg.add_text(i18n["visited_locations"])
                    add_help(i18n["locations_list_info"])

                    dpg.add_input_text(
                        hint=i18n["search"],
                        tag="location_filter",
                        callback=self.filter_search
                    )
                    dpg.add_listbox(
                        tag="location_names",
                        num_items=12,
                        callback=self.select_location
                    )
                    dpg.add_button(
                        label=i18n["add"],
                        callback=lambda _: dpg.configure_item(
                            "add_location",
                            show=True
                        )
                    )

                # Location stats
                with dpg.group():
                    dpg.add_text(i18n["location_information"])
                    add_help(i18n["time_measured_in_frames_info"])

                    with dpg.child_window(
                        tag="stats",
                        border=False,
                        show=False,
                        no_scrollbar=True
                    ):
                        # Time values
                        for time_value in stats["time_values"]:
                            dpg.add_input_int(
                                label=i18n["location_stats"][
                                    stats["time_values"][time_value]
                                ],
                                tag=time_value,
                                width=200 * SCALE,
                                callback=self.change,
                                user_data=time_value
                            )
                        
                        dpg.add_separator()
                        dpg.add_text(i18n["average_run_data"])

                        # Average values
                        for average_value in stats["average_values"]:
                            dpg.add_input_double(
                                label=i18n["location_stats"][
                                    stats["average_values"][average_value]
                                ],
                                tag=average_value,
                                width=200 * SCALE,
                                callback=self.change,
                                user_data=average_value
                            )

                        add_help(i18n["location_resources_info"])

                        # Damage
                        dpg.add_separator()
                        dpg.add_text(i18n["damage"])

                        for damage_value in stats["damage_values"]:
                            dpg.add_input_double(
                                label=i18n["location_stats"][
                                    stats["damage_values"][damage_value]
                                ],
                                tag=damage_value,
                                width=200 * SCALE,
                                callback=self.change,
                                user_data=damage_value
                            )

                        # Element damage
                        dpg.add_separator()
                        dpg.add_text(i18n["element_damage"])
                        add_help(i18n["element_damage_affect_on_rune_info"])

                        for element_damage_type in stats["element_damage_values"]:
                            dpg.add_input_double(
                                label=i18n["location_stats"][
                                    stats["element_damage_values"][element_damage_type]
                                ],
                                tag=element_damage_type,
                                width=200 * SCALE,
                                callback=self.change,
                                user_data=element_damage_type
                            )
