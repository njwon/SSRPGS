import dearpygui.dearpygui as dpg
from json import dumps
from math import log2

class InventoryItem:
    abbrs = {
        "hI": "Взаимодействован",
        "lv": "Уровень",
        "el": "Элемент",
        "abs": "Дополнительные способности",
        "ra": "Чары",
        "rng": "Сид",
        "sh": "Блёстки",
        "lC": "Уровень",
        "lBU": "Прокачек",
        "tag": "Тег",
        "sig": "Сигнатура",
        "c": "Индекс косметики",
        "ql": "Качество",
        "sSS": "Сид",
        "": "",
        # Potions
        "potion_type": "Тип зелья",
        "last_type": "Последний тип",
        "auto_refill": "Перезалив",
        "costs": "Затраты",
        "resource": "Ресурс",
        "amount": "Количество",
        "itemId": "Id предмета",
        "level": "Уровень",
        "requiresFlag": "Требует",
        "blockedByFlag": "Блокирован",
        "": "",
        # Treasure
        "rS": "Случайный суффикс",
        "itms": "Предметы",
        "id": "Предмет",
        "t": "Тип",
        "e": "Элемент",
    }

    def get_abbr_description(abbr):
        if abbr in InventoryItem.abbrs:
            return InventoryItem.abbrs[abbr]
        else:
            return abbr

class InventoryTab:
    def __init__(self, save):
        self.save = save
        self.last_opened_item_index = None

    def load(self):
        dpg.delete_item("item_settings", children_only=True)
        inventory_item_names = self.generate_items_list()
        dpg.configure_item("inventory", items=inventory_item_names)

        if inventory_item_names:
            self.open_item("load", inventory_item_names[0])

    def dump(self):
        pass

    def generate_items_list(self, filter_key=False):
        items = self.save["progress_data"]["inventory_data"]["itms"]
        inventory_item_names = []

        for i, item in enumerate(items):
            if (filter_key and filter_key in item["id"]) or not filter_key:
                inventory_item_names.append(
                    f"{item["id"]}".ljust(95) + f"{i}"
                )

        return inventory_item_names
    
    def change(self, _, value, path):
        print(f"going to change {value=} on {path=} ({_=}) imt={self.save["progress_data"]["inventory_data"]["itms"][self.last_opened_item_index]}")

        head = self.save["progress_data"]["inventory_data"]["itms"][self.last_opened_item_index]

        for key in path[:-1]:
            head = head[key]

        print(head)
        head[path[-1]] = value

        print("Changes smthing...: ", self.save["progress_data"]["inventory_data"]["itms"][self.last_opened_item_index])

    def travel(self, item, start_path=None):
        if start_path is None:
            print("start_path is None, swithing on []")
            start_path = []

        for key, value in item.items() if isinstance(item, dict) else enumerate(item):
            path = start_path[:]
            path.append(key)
            print(item, start_path, path, key, value)

            match value:
                case dict():
                    self.travel(value, path)
                case list():
                    self.travel(value, path)
                case bool():
                    dpg.add_checkbox(label=key, default_value=value, parent="item_settings", callback=self.change, user_data=path)
                case str():
                    dpg.add_input_text(label=key, default_value=value, parent="item_settings", callback=self.change, user_data=path)
                case int():
                    dpg.add_input_int(label=key, default_value=value,parent="item_settings", callback=self.change, user_data=path)


    def filter_items(self, _, filter_key):
        if not self.save.is_loaded():
            return
        
        inventory_item_names = self.generate_items_list(filter_key)
        dpg.configure_item("inventory", items=inventory_item_names)
        
        if inventory_item_names:
            self.open_item(_, inventory_item_names[0])
    
    # def make_input_value(self, key, value, group="item_settings", trace=None):
    #     label = InventoryItem.get_abbr_description(key)
        
    #     match value:
    #         case bool():
    #             dpg.add_checkbox(label=label, default_value=value, parent=group)
            
    #         case int():
    #             dpg.add_input_int(label=label, width=200, default_value=value, parent=group)
            
    #         case str():
    #             dpg.add_input_text(label=label, width=200, default_value=value, parent=group)

    #         case list():
    #             if isinstance(value[0], str):
    #                 dpg.add_text(label, parent=group, tag=label)
    #                 dpg.add_input_text(multiline=True, default_value="\n".join(value) + "\n", width=400, parent=group, height=64)
    #                 dpg.add_separator(parent=group)
    #             else:
    #                 dpg.add_text(label, parent=group)
    #                 for i, folded_value in enumerate(value):
    #                     self.make_input_value(f"obj_{i}", folded_value)

    #         case dict():
    #             dpg.add_text(label, parent=group, tag=label)
    #             for folded_key in value:
    #                 self.make_input_value(folded_key, value[folded_key])
    #             dpg.add_separator(parent=group)

    def open_item(self, _, item):
        # Save data
        # ...

        dpg.delete_item("item_settings", children_only=True)
        
        # Recursevly parse all item setting dict
        self.last_opened_item_index = int(item.split()[-1])
        item = self.save["progress_data"]["inventory_data"]["itms"][self.last_opened_item_index]

        item_repr = dumps(item, indent=4)
        

        self.travel(item)
        # dpg.add_input_text(label="Название", width=200, default_value=item["id"], parent="item_settings")
        # dpg.add_input_int(label="Количество", width=200, default_value=item["co"] if "co" in item else 1, parent="item_settings")

        # if "da" not in item:
        #     print(f"Item {item["id"]} has no data")
        #     return
        
        # for key in item["da"]:
        #     self.make_input_value(key, item["da"][key])
        
        # Json
        dpg.add_separator(parent="item_settings")
        dpg.add_text("Json представление", parent="item_settings")
        dpg.add_input_text(default_value=item_repr, multiline=True, parent="item_settings", width=400, height=412-96)
   
    def gui(self):
        with dpg.group(horizontal=True):
                with dpg.group(width=175):
                    dpg.add_text("Предметы")
                    dpg.add_input_text(callback=self.filter_items)
                    dpg.add_listbox(tag="inventory", num_items=12, callback=self.open_item)
                    dpg.add_button(label="Создать предмет")

                with dpg.child_window(border=False, no_scrollbar=True):
                    dpg.add_text("Данные предмета", tag="item_info")

                    dpg.add_group(tag="item_settings")  # conrainer for item setting
