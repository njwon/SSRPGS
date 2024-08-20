import dearpygui.dearpygui as dpg
from pyperclip import copy, paste
import json

from translations import *
from utils import add_help

REMAP_START = 0x10ec77

items = {
    "Top": {
        "name": "",
        "fields": {
            "id": "name",
            "co": "count",
            "da": "data",
        }
    },
    "Style": {
        "name": "style",
        "fields": {
            "da hI": "has_interacted",
            "da sh": "shiny",
            "da c": "cosmetics",
            "da tag": "tag",
            "da sig": "signature",
        }
    },
    "Improvements": {
        "name": "improvements",
        "fields": {
            "da lv": "level",
            "da lC": "lost_item_elements",
            "da lBU": "lost_item_upgrades",
            "da el": "element",
        }
    },
    "Effects": {
        "name": "effects",
        "fields": {
            "da abs": "effects",
        }
    },
    "Items": {
        "name": "items_list",
        "fields": {
            "da itms": "items",
            "da itms _ id": "name",
            "da itms _ t": "rarity_type",
            "da itms _ lv": "level",
            "da itms _ min": "minimum",
            "da itms _ max": "maximum",
            "da itms _ rng": "random_seed",
            "da itms _ e": "element",
        }
    },
    "Enchantments": {
        "name": "enchantments",
        "fields": {
            "da ra": "enchantments",
            "da ra lv": "enchantments_level",
            "da ra ql": "enchantments_quality",
            "da ra sSS": "enchantments_seed",
        }
    },
    "RNG's": {
        "name": "seeds",
        "fields": {
            "da rng": "random_seed",
            "da rS": "random_suffix",
        }
    },
    "Potion": {
        "name": "potion",
        "fields": {
            "da potion_type": "potion_type",
            "da last_type": "last_type",
            "da auto_refill": "auto_refill",
        }
    },
    "Costs": {
        "name": "costs",
        "fields": {
            "da costs": "costs",
            "da costs _ resource": "resource",
            "da costs _ amount": "amount",
            "da costs _ itemId": "item_name",
            "da costs _ level": "level",
        }
    }
}

fields = {
    "co": 1,
    "da lv": 1,
    "da hI": True,
    "da sig": "",
    "da sh": True,
    "da c": "",
    "da ra": {"lv": 21, "ql": 12049, "sSS": 0},
    "da abs": [""],
    "da abs _": "",
}

sorting_order = [
    # Top level
    "id",
    "co",
    "da",
    # Item info
    "hI",
    "sh",
    "c",
    "co",
    "tag",
    "sig",
    # Item level
    "lv",
    "el",
    "lC",
    "lBU",
    # Chest items
    "itms",
    "t",
    "e",
    "showC",
    "rB",
    "min",
    "max",
    # Enchantments
    "ra",
    "ql",
    "sSS",
    # RNG seeds
    "rng",
    "rS",
]

class InventoryTab:
    def __init__(self, save):
        self.save = save
        self.items = None

        self.item_groups = set()
        self.item_index = None
        self.item = None

    def load(self):
        self.items = self.save["progress_data"]["inventory_data"]["itms"]
        self.filter_search("load", dpg.get_value("item_filter"))

    def filter_search(self, _, filter_key="", no_open=False):
        if not self.save.is_loaded():
            return

        item_names = self.generate_items_names(filter_key)
        dpg.configure_item("inventory", items=item_names)

        if not len(item_names):
            dpg.delete_item("item_settings", children_only=True)
            return

        if not no_open:
            self.open_item(_, dpg.get_value("inventory"))

    def add_ensure_one_separator(self):
        last_item_type = dpg.get_item_type(dpg.last_item())

        if last_item_type != "mvAppItemType::mvSeparator":
            dpg.add_separator(parent="item_settings")

    def sorting(self, item):
        def sorter(value):
            key, value = value

            if key in sorting_order:
                return sorting_order.index(key)
            else:
                return len(sorting_order) - 3

        sorted_items_pairs = []
        for key, value in item.items():
            if isinstance(value, dict):
                value = self.sorting(value)
            elif isinstance(value, list) and isinstance(value[0], dict):  # List of dicts
                value = [self.sorting(i) for i in value]

            sorted_items_pairs.append((key, value))
            sorted_items_pairs = sorted(sorted_items_pairs, key=sorter)

        sorted_dict = dict(sorted_items_pairs)

        return sorted_dict

    def generate_items_names(self, filter_key=""):
        items_names = []

        for i, item in enumerate(self.items):
            if filter_key in item["id"]:
                items_names.append(
                    f"{item["id"]}{chr(i + REMAP_START)}"
                )

        return items_names

    def check_group_label(self, group):
        group = str(group)  # Convert TranslationDict to str

        if group not in self.item_groups:
            self.item_groups.add(group)

            self.add_ensure_one_separator()
            dpg.add_text(group, parent="item_settings")
    
    def match_path(self, path, match_path):
        match_path = match_path.split()

        if len(path) != len(match_path):
            return False

        for a, b in zip(path, match_path):
            if a != b and b != "_":
                return False
            
        return True

    def get_label(self, path):
        for group in items:
            for field in items[group]["fields"]:
                if self.match_path(path, field):
                    if items[group]["name"]:
                        self.check_group_label(
                            i18n["item_info"][items[group]["name"]]
                        )
                    return i18n["item_info"][items[group]["fields"][field]]
        
        return path[-1]
    
    def change(self, _, value, path):
        # Pointer on last object inside of a dict
        head = self.item
        for key in path[:-1]:
            head = head[key]

        head[path[-1]] = value

        # Update item name if it was changed
        if path == ["id"]:
            item_names = self.generate_items_names(
                dpg.get_value("item_filter")
            )
            dpg.configure_item(
                "inventory",
                items=item_names,
                default_value=f"{self.item["id"]}{chr(self.item_index + REMAP_START)}"
            )

        print(f"Changed field: {path[-1]}: {head[path[-1]]}")
    
    def add_field(self, _, value=None, path=None):
        if not self.item:
            return
        
        if not path:
            field = ord(dpg.get_value("add_field_name")[-1]) - REMAP_START
            path = list(fields)[field]

        default_value = fields[path]
        if isinstance(default_value, (dict, list)):
            default_value = fields[path].copy()

        # Ensure that trace available
        if "da" not in self.item:
            self.item["da"] = {}

        path = path.split()
        head = self.item
        for key in path[:-1]:
            head = head[key]

        if path[-1] == "_":
            head.append(default_value)
        else:
            head[path[-1]] = default_value
        print(f"Created field {path} with value of {default_value}")

        self.open_item(_, chr(self.item_index + REMAP_START))
        dpg.configure_item("add_field", show=False)

    def remove(self, _, value, path):
        # Pointer on last object inside of a dict
        head = self.item
        parent = self.item
        for key in path[:-1]:
            parent = head
            head = head[key]

        if path == ['id']:  # Delete all item
            deleted_item = self.items.pop(self.item_index)
            print(f"Deleted item: {deleted_item["id"]}")

            dpg.configure_item("inventory", default_value="")
            self.filter_search("remove", dpg.get_value("item_filter"))

            return

        if len(head) == 1:  # Iterable with one item
            if len(path) > 1:
                del parent[path[-2]]
        else:
            del head[path[-1]]

        self.open_item("remove", chr(self.item_index + REMAP_START))
        print(f"Deleted field: {path[-1]}")

    def travel(self, item, start_path=None):
        if start_path is None:
            start_path = []

        items = item.items() if isinstance(item, dict) else enumerate(item)
        for key, value in items:
            path = start_path[:]
            path.append(key)
            key_label = self.get_label(path)

            match value:
                case dict():
                    self.travel(value, path)
                case list():
                    self.travel(value, path)
                    if path[-1] == "abs":
                        dpg.add_button(
                            label="+",
                            parent="item_settings",
                            callback=self.add_field,
                            user_data=" ".join(path) + " _"
                        )

                case bool():
                    with dpg.group(horizontal=True, parent="item_settings"):
                        dpg.add_button(
                            label="X",
                            callback=self.remove,
                            user_data=path
                        )
                        dpg.add_checkbox(
                            label=key_label,
                            default_value=value,
                            callback=self.change,
                            user_data=path
                        )
                case str():
                    with dpg.group(horizontal=True, parent="item_settings"):
                        dpg.add_button(
                            label="X",
                            callback=self.remove,
                            user_data=path
                        )
                        dpg.add_input_text(
                            label=key_label,
                            default_value=value,
                            callback=self.change,
                            user_data=path
                        )
                case int():
                    with dpg.group(horizontal=True, parent="item_settings"):
                        dpg.add_button(
                            label="X",
                            callback=self.remove,
                            user_data=path
                        )
                        dpg.add_input_int(
                            label=key_label,
                            default_value=value,
                            callback=self.change,
                            user_data=path
                        )

            if isinstance(item, list) and isinstance(item[0], dict):
                self.add_ensure_one_separator()

    def paste(self):
        try:
            item = json.loads(paste())
            print(f"Pasted item {item}")
        except json.JSONDecodeError:
            print("Wrong item json code")
            return

        self.items[self.item_index] = item
        self.item = self.items[self.item_index]
        self.filter_search("paste")

    def open_item(self, _, item):
        dpg.delete_item("item_settings", children_only=True)
        
        self.item_groups = set()
        self.item_index = ord(item[-1]) - REMAP_START
        self.item = self.items[self.item_index]

        self.travel(self.sorting(self.item))
        self.create_item_settings()

        print(f"Selected item: {self.item["id"]}")

    def add_item(self, _):
        if not self.save.is_loaded():
            return

        dpg.configure_item("item_filter", default_value="")

        self.items.insert(0, {"id": "new_item", "co": 1, "da": {"hI": False}})
        self.filter_search("load")

    def create_item_settings(self):
        with dpg.group(
            parent="item_settings",
        ):
            dpg.add_separator()
            dpg.add_text(i18n["management"])
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label=i18n["add_field"],
                    callback=lambda _: dpg.configure_item(
                        "add_field",
                        show=True
                    )
                )
                dpg.add_button(
                    label=i18n["copy_code"],
                    callback=lambda _: copy(
                        json.dumps(self.item, ensure_ascii=False)
                    )
                )
                dpg.add_button(
                    label=i18n["paste_code"],
                    callback=self.paste,
                )

    def gui(self):
        fields_names = []
        for i, field in enumerate(fields):
            for group in items:
                if field in items[group]["fields"]:
                    fields_names.append(
                        i18n["item_info"][
                            items[group]["fields"][field]
                        ] + chr(i + REMAP_START)
                    )

        # Add field to item
        with dpg.window(
            label=i18n["add_field"],
            pos=((600 - 350) // 2, (394 - 86) // 2),
            width=350,
            height=86,
            min_size=(350, 0),
            show=False,
            tag="add_field"
        ):
            dpg.add_combo(
                label=i18n["field"],
                width=200,
                items=fields_names,
                default_value=fields_names[0],
                tag="add_field_name"
            )

            with dpg.group(horizontal=True):
                dpg.add_button(
                    label=i18n["add"],
                    callback=self.add_field
                )
                dpg.add_button(
                    label=i18n["cancel"],
                    callback=lambda _: dpg.configure_item(
                        "add_field",
                        show=False
                    )
                )

        with dpg.group(horizontal=True):
            # List of available items
            with dpg.group(width=175):
                dpg.add_text(i18n["items"])
                dpg.add_input_text(
                    tag="item_filter",
                    hint=i18n["search"],
                    callback=self.filter_search
                )
                dpg.add_listbox(
                    tag="inventory",
                    num_items=12,
                    callback=self.open_item
                )
                dpg.add_button(
                    label=i18n["create_item"],
                    callback=self.add_item
                )

            # Item info
            with dpg.child_window(border=False, no_scrollbar=True):
                dpg.add_text(i18n["item_data"], tag="item_info")
                dpg.add_child_window(
                    height=303,
                    border=False,
                    no_scrollbar=True,
                    tag="item_settings"
                )  # Conrainer for item setting
