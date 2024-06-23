import dearpygui.dearpygui as dpg
from math import log2

class InventoryItem():
    def __init__(self, index, data):
        self.index = index
        self.data = data

    def __repr__(self):
        count = "x1"
        level = ""
        enchantment_level = ""
        element = ""
        
        if "da" in self.data:
            if "lv" in self.data["da"]:
                if "_stone" in self.data["id"]:
                    level = f" *{self.data["da"]["lv"]}"
                else:
                    level = f" *{round(log2(self.data["da"]["lv"]))}"
            
            if "ra" in self.data["da"]:
                enchantment_level = f" +{self.data["da"]["ra"]["lv"]}"
        
            if "el" in self.data["da"]:
                element = " " + self.data["da"]["el"]

        if "co" in self.data:
            count = f"x{self.data["co"]}"

        return f"{self.data["id"]}".ljust(95) + f"{self.index}".ljust(5)
    
    def get_data(self):
        return self.data

class InventoryTab:
    def __init__(self, save):
        self.save = save
    
    def load(self):
        inventory_item_names = [InventoryItem(i, item) for i, item in enumerate(self.save["progress_data"]["inventory_data"]["itms"])]
        dpg.configure_item("inventory", items=inventory_item_names)

    def dump(self):
        pass

    def filter_items(self, _, key):
        if not self.save.is_loaded():
            return
        
        items = [InventoryItem(i, item) for i, item in enumerate(self.save["progress_data"]["inventory_data"]["itms"])]
        inventory_item_names = list(filter(lambda item: key in item.__repr__(), items))

        dpg.configure_item("inventory", items=inventory_item_names)
    
    def open_item(self, _, item):
        # Save data
        # ...

        dpg.delete_item("item_settings", children_only=True)
        
        # Recursevly parse all item setting dict
        item = self.save["progress_data"]["inventory_data"]["itms"][int(item.split()[-1])]

        dpg.add_input_text(label="Название", default_value=item["id"], parent="item_settings")
        dpg.add_input_int(label="Количество", default_value=item["co"] if "co" in item else 1, parent="item_settings")

        if "da" in item:
            dpg.add_separator(parent="item_settings")
            dpg.add_text("Данные", parent="item_settings")
            
            for key in item["da"]:
                match item["da"][key]:
                    case int():
                        dpg.add_input_int(label=key, default_value=item["da"][key], parent="item_settings")
                    case str():
                        dpg.add_input_text(label=key, default_value=item["da"][key], parent="item_settings")
                    case list():
                        dpg.add_input_text(label=key+"**", default_value=item["da"][key], parent="item_settings")
        
    def gui(self):
        with dpg.group(horizontal=True):
                with dpg.group(width=175):
                    dpg.add_text("Предметы")
                    dpg.add_input_text(callback=self.filter_items)
                    dpg.add_listbox(tag="inventory", num_items=12, callback=self.open_item)
                    dpg.add_button(label="Создать предмет")

                with dpg.group(width=200):
                    dpg.add_text("Данные предмета", tag="item_info")

                    dpg.add_group(tag="item_settings")  # conrainer for item setting
