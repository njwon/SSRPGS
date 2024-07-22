import dearpygui.dearpygui as dpg

items = {
    "Top": {
        "name": "",
        "fields": {
            "id": "Название",
            "co": "Количество",
            "da": "Данные",
        }
    },
    "Style": {
        "name": "Вид",
        "fields": {
            "da hI": "Взаимодействован",
            "da sh": "Блёстки",
            "da c": "Вид косметики",
            "da tag": "Тег",
            "da sig": "Сигнатура",
        }
    },
    "Improvements": {
        "name": "Улучшение",
        "fields": {
            "da lv": "Уровень",
            "da lC": "Элементов",
            "da lBU": "Улучшений",
            "da el": "Элемент",
        }
    },
    "Effects": {
        "name": "Эффекты",
        "fields": {
            "da abs": "Эффекты",
        }
    },
    "Items": {
        "name": "Список предметов",
        "fields": {
            "da itms": "Предметы",
            "da itms _ id": "Название",
            "da itms _ t": "Тип редкости",
            "da itms _ lv": "Уровень",
            "da itms _ min": "Минимум",
            "da itms _ max": "Максимум",
            "da itms _ rng": "Случайный сид",
            "da itms _ e": "Элемент",
        }
    },
    "Enchantments": {
        "name": "Чары",
        "fields": {
            "da ra": "Чары",
            "da ra lv": "Уровень чар",
            "da ra ql": "Качество чар",
            "da ra sSS": "Сид чар",
        }
    },
    "RNG's": {
        "name": "Сиды",
        "fields": {
            "da rng": "Случайный сид",
            "da rS": "Случайный суффикс",
        }
    },
    "Potion": {
        "name": "Зелье",
        "fields": {
            "da potion_type": "Тип",
            "da last_type": "Последний тип",
            "da auto_refill": "Перезалив",
        }
    },
    "Costs": {
        "name": "Затраты",
        "fields": {
            "da costs": "Затраты",
            "da costs _ resource": "Ресурс",
            "da costs _ amount": "Количество",
            "da costs _ itemId": "Предмет",
            "da costs _ level": "Уровень",
        }
    }
}

fields = {
    "da co": 0,
    "da hI": True,
    "da sig": "",
    "da hI": True,
    "da sh": True,
    "da c": "",
    "da tag": "",
    "da sig": "",
    "da ra": {"lv": 21, "ql": 12049, "sSS": 99048},
    "da abs": [],
}

class InventoryTab:
    def __init__(self, save):
        self.save = save
        self.items = None

        self.item_groups = set()
        self.item_index = None
        self.item = None

    def load(self):
        self.items = self.save["progress_data"]["inventory_data"]["itms"]
        self.filter_items("load", dpg.get_value("search_filter"))

    def add_ensure_one_separator(self):
        last_item_type = dpg.get_item_type(dpg.last_item())

        if last_item_type != "mvAppItemType::mvSeparator":
            dpg.add_separator(parent="item_settings")

    def sorter(self, value):
            stats = [
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

            key, value = value
            return stats.index(key) if key in stats else len(stats) - 3
    
    def sorting(self, item):
        sorted_dict_items = []

        for key, value in item.items():
            if isinstance(value, dict):
                value = self.sorting(value)
            elif isinstance(value, list) and isinstance(value[0], dict):  # List of dicts
                value = [self.sorting(i) for i in value]
        
            sorted_dict_items.append((key, value))
            sorted_dict_items = sorted(sorted_dict_items, key=self.sorter)
        
        sorted_dict = dict(sorted_dict_items)

        return sorted_dict

    def generate_items_names(self, filter_key=False):
        items_names = []

        for i, item in enumerate(self.items):
            if (filter_key and filter_key in item["id"]) or not filter_key:
                items_names.append(
                    f"{item["id"]}{chr(i + 0x10ec77)}"
                )

        return items_names
    
    def check_group_label(self, group):
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
                        self.check_group_label(items[group]["name"])
                    return items[group]["fields"][field]
        
        return path[-1]
    
    def change(self, _, value, path):
        # Pointer on last object inside of a dict
        head = self.item
        for key in path[:-1]:
            head = head[key]

        head[path[-1]] = value

        # Update item name if it was changed
        if path == ["id"]:
            item_names = self.generate_items_names()
            dpg.configure_item("inventory", items=item_names)
            dpg.configure_item("inventory", default_value=f"{self.item["id"]}{chr(self.item_index + 0x10ec77)}")

        print(f"Changed field: {path[-1]}: {head[path[-1]]}")
    
    def add_field(self, _):
        if not self.item:
            return
        
        field = ord(dpg.get_value("add_field_name")[-1]) - 0x10ec77

        path = list(fields)[field]
        default_value = fields[path]

        if isinstance(default_value, (dict, list)):
            default_value = fields[path].copy()

        path = path.split()
        head = self.item
        for key in path[:-1]:
            head = head[key]

        head[path[-1]] = default_value
        print(self.item)
        self.open_item(_, chr(self.item_index + 0x10ec77))
        dpg.configure_item("add_field", show=False)

    def remove(self, _, value, path):
        # Pointer on last object inside of a dict
        head = self.item
        parent = self.item
        for key in path[:-1]:
            parent = head
            head = head[key]
        
        if path == ['id']:  # Delete all item
            print(f"Deleted {self.items.pop(self.item_index)["id"]}")

            dpg.delete_item("item_settings", children_only=True)
            self.load()
            return

        if len(head) == 1:  # Iterable with one item
            if len(path) > 1:
                del parent[path[-2]]
        else:
            del head[path[-1]]

        self.open_item(_, chr(self.item_index + 0x10ec77))
        print(f"Deleted field {path[-1]}")

    def travel(self, item, start_path=None):
        if start_path is None:
            start_path = []

        for key, value in item.items() if isinstance(item, dict) else enumerate(item):
            path = start_path[:]
            path.append(key)
            key_label = self.get_label(path)

            match value:
                case dict():
                    self.travel(value, path)
                case list():
                    self.travel(value, path)
                case bool():
                    with dpg.group(horizontal=True, parent="item_settings"):
                        dpg.add_button(label="X", callback=self.remove, user_data=path)
                        dpg.add_checkbox(label=key_label, default_value=value, callback=self.change, user_data=path)
                case str():
                    with dpg.group(horizontal=True, parent="item_settings"):
                        dpg.add_button(label="X", callback=self.remove, user_data=path)
                        dpg.add_input_text(label=key_label, default_value=value, callback=self.change, user_data=path)
                case int():
                    with dpg.group(horizontal=True, parent="item_settings"):
                        dpg.add_button(label="X", callback=self.remove, user_data=path)
                        dpg.add_input_int(label=key_label, default_value=value, callback=self.change, user_data=path)

            if isinstance(item, list) and isinstance(item[0], dict):
                self.add_ensure_one_separator()

    def filter_items(self, _, filter_key):
        if not self.save.is_loaded():
            return
        
        item_names = self.generate_items_names(filter_key)
        last_selected_item = dpg.get_value("inventory")

        dpg.configure_item("inventory", items=item_names)
        print(f"Filtering inventory by key: '{filter_key}'")

        if len(item_names) and last_selected_item not in item_names:
            self.open_item(_, item_names[0])

    def open_item(self, _, item):
        dpg.delete_item("item_settings", children_only=True)
        
        self.item_groups = set()
        self.item_index = ord(item[-1]) - 0x10ec77
        self.item = self.items[self.item_index]

        self.travel(self.sorting(self.item))
        print(f"Selected item: {self.item}")

    def add_item(self, _):
        item = {
            "id": "new_item",
            "co": 1,
            "da": {
                "hI": False,
            }
        }

        self.items.insert(0, item)
        self.load()

    def gui(self):
        fields_names = []
        for i, field in enumerate(fields):
            for group in items:
                if field in items[group]["fields"]:
                    fields_names.append(items[group]["fields"][field] + chr(i + 0x10ec77))

        with dpg.window(
            label="Добавить поле",
            pos=((600 - 350) // 2, (400 - 140) // 2),
            width=350,
            height=140,
            show=False,
            tag="add_field"
        ):
            dpg.add_combo(
                label="Поле",
                width=200,
                items=fields_names,
                default_value=fields_names[0],
                tag="add_field_name"
            )
            
            with dpg.group(horizontal=True):
                dpg.add_button(label="Добавить", callback=self.add_field)
                dpg.add_button(label="Отменить", callback=lambda _: dpg.configure_item("add_field", show=False))

        with dpg.group(horizontal=True):
                with dpg.group(width=175):
                    dpg.add_text("Предметы")
                    dpg.add_input_text(tag="search_filter", hint="Поиск", callback=self.filter_items)
                    dpg.add_listbox(tag="inventory", num_items=12, callback=self.open_item)
                    dpg.add_button(label="Создать предмет", callback=self.add_item)

                with dpg.child_window(border=False, no_scrollbar=True):
                    dpg.add_text("Данные предмета", tag="item_info")

                    dpg.add_child_window(
                        height=277,
                        border=False,
                        no_scrollbar=True,
                        tag="item_settings"
                    ) # conrainer for item setting
                    
                    with dpg.child_window(
                        border=False,
                        no_scrollbar=True,
                    ):
                        with dpg.group(horizontal=True):
                            dpg.add_button(label="Добавить поле", callback=lambda _: dpg.configure_item("add_field", show=True))
