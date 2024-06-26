import dearpygui.dearpygui as dpg
from json import dumps
from math import log2

class InventoryTab:
    def __init__(self, save):
        self.save = save

        self.items = None
        self.item = None
        self.item_groups = set()

    def load(self):        
        self.items = self.save["progress_data"]["inventory_data"]["itms"]
        item_names = self.generate_items_list()

        dpg.configure_item("inventory", items=item_names)

        if item_names:
            self.open_item("load", item_names[0])

    def add_ensure_one_separator(self):
        last_item = dpg.get_item_type(dpg.last_item())

        if last_item != "mvAppItemType::mvSeparator":
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
                # Enchants
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

    def generate_items_list(self, filter_key=False):
        items_names = []

        for i, item in enumerate(self.items):
            if (filter_key and filter_key in item["id"]) or not filter_key:
                items_names.append(
                    f"{item["id"]}{chr(i)}"  # HERE WILL BE A GIANT CRUTCH
                )

        return items_names
    
    def check_group_label(self, group):
        if group not in self.item_groups:
            self.item_groups.add(group)

            self.add_ensure_one_separator()
            dpg.add_text(group, parent="item_settings")
    
    def get_label(self, path):
        match path:
            # Top level
            case ("id",):
                return "Название"
            case ("co",):
                return "Количество"
            case ("da",):
                return "Данные"
            
            # Style
            case ("da", "hI"):
                self.check_group_label("Вид")
                return "Взаимодействован"
            case ("da", "sh"):
                self.check_group_label("Вид")
                return "Блёстки"
            case ("da", "c"):
                self.check_group_label("Вид")
                return "Вид косметики"
            case ("da", "tag"):
                self.check_group_label("Вид")
                return "Тег"
            case ("da", "sig"):
                self.check_group_label("Вид")
                return "Сигнатура"
            
            # Item improvement info
            case ("da", "lv"):
                self.check_group_label("Прокачка")
                return "Уровень"
            case ("da", "lC"):
                return "Элементов"
            case ("da", "lBU"):
                return "Улучшений"
            case ("da", "el"):
                return "Элемент"
            
            case ("da", "abs"):
                self.check_group_label("Эффекты")
                return "Эффекты"
            
            # Itmes list in chest
            case ("da", "itms"):
                self.check_group_label("Список предметов")
                return "Предметы"
            case ("da", "itms", _, "id"):
                return "Название"
            case ("da", "itms", _, "t"):
                return "Тип редкости"
            case ("da", "itms", _, "lv"):
                return "Уровень"
            case ("da", "itms", _, "min"):
                return "Минимум"
            case ("da", "itms", _, "max"):
                return "Максимум"
            case ("da", "itms", _, "rng"):
                return "Случайный сид"
            case ("da", "itms", _, "e"):
                return "Элемент"
            
            # Enchantments
            case ("da", "ra"):
                self.check_group_label("Чары")
                return "Чары"
            case ("da", "ra", "lv"):
                return "Уровень чар"
            case ("da", "ra", "ql"):
                return "Качество чар"
            case ("da", "ra", "sSS"):
                return "Сид чар"
            
            # RNG's
            case ("da", "rng"):    
                self.check_group_label("Сиды")
                return "Случайный сид"
            case ("da", "rS"):
                self.check_group_label("Сиды")
                return "Случайный суффикс"
            
            # Potion
            case ("da", "potion_type"):
                self.check_group_label("Зелье")
                return "Тип"
            case ("da", "last_type"):
                return "Последний тип"
            case ("da", "auto_refill"):
                return "Перезалив"
            
            # Potions costs
            case ("da", "costs"):
                self.check_group_label("Затраты")
                return "Затраты"
            case ("da", "costs", _, "resource"):
                return "Ресурс"
            case ("da", "costs", _, "amount"):
                return "Количество"
            case ("da", "costs", _, "itemId"):
                return "Предмет"
            case ("da", "costs", _, "level"):
                return "Уровень"

            case _:
                return path[-1]
    
    def change(self, _, value, path):
        # Pointer on last object inside of a dict
        head = self.item
        for key in path[:-1]:
            head = head[key]
        
        head[path[-1]] = value

        print("Changed item: ", self.item)

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
                    dpg.add_checkbox(label=key_label, default_value=value, parent="item_settings", callback=self.change, user_data=path)
                case str():
                    dpg.add_input_text(label=key_label, default_value=value, parent="item_settings", callback=self.change, user_data=path)
                case int():
                    dpg.add_input_int(label=key_label, default_value=value,parent="item_settings", callback=self.change, user_data=path)

            if isinstance(item, list) and isinstance(item[0], dict):
                self.add_ensure_one_separator()

    def filter_items(self, _, filter_key):
        if not self.save.is_loaded():
            return
        
        item_names = self.generate_items_list(filter_key)
        last_selected_item = dpg.get_value("inventory")

        dpg.configure_item("inventory", items=item_names)
        if len(item_names) and last_selected_item not in item_names:
            self.open_item(_, item_names[0])

    def open_item(self, _, item):
        dpg.delete_item("item_settings", children_only=True)
        
        self.item_groups = set()
        self.item = self.items[ord(item[-1])]

        self.travel(self.sorting(self.item))
   
    def gui(self):
        with dpg.group(horizontal=True):
                with dpg.group(width=175):
                    dpg.add_text("Предметы")
                    dpg.add_input_text(hint="Поиск", callback=self.filter_items)
                    dpg.add_listbox(tag="inventory", num_items=12, callback=self.open_item)
                    dpg.add_button(label="Создать предмет")

                with dpg.child_window(border=False, no_scrollbar=True):
                    dpg.add_text("Данные предмета", tag="item_info")

                    dpg.add_group(tag="item_settings")  # conrainer for item setting
