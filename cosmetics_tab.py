import dearpygui.dearpygui as dpg

items = [
    'aether_talisman:AEther',
    'fire_talisman:Fire',
    'bardiche',
    'bashing_shield',
    'blade_of_god',
    'compound_shield',
    'crossbow',
    'cult_mask',
    'crusader_shield:Vigor',
    'dashing_shield',
    'heavy_hammer',
    'quarterstaff',
    'repeating_crossbow',
    'shield',
    'skeleton_arm',
    'socketed_crossbow:AEther',
    'socketed_crossbow:Fire',
    'socketed_crossbow:Ice',
    'socketed_crossbow:Poison',
    'socketed_crossbow:Vigor',
    'socketed_hammer:AEther',
    'socketed_hammer:Fire',
    'socketed_hammer:Ice',
    'socketed_hammer:Poison',
    'socketed_hammer:Vigor',
    'socketed_long_sword:AEther',
    'socketed_long_sword:Fire',
    'socketed_long_sword:Ice',
    'socketed_long_sword:Poison',
    'socketed_long_sword:Vigor',
    'socketed_shield:AEther',
    'socketed_shield:Fire',
    'socketed_shield:Ice',
    'socketed_shield:Poison',
    'socketed_shield:Vigor',
    'socketed_staff',
    'socketed_staff:AEther',
    'socketed_staff:Fire',
    'socketed_staff:Ice',
    'socketed_staff:Poison',
    'socketed_staff:Vigor',
    'socketed_sword:AEther',
    'socketed_sword:Fire',
    'socketed_sword:Ice',
    'socketed_sword:Poison',
    'socketed_sword:Vigor',
    'sword',
    'tower_shield',
    'wand',
    'wand:AEther',
    'wand:Fire',
    'wand:Ice',
    'wand:Poison',
    'wand:Vigor'
]

class CosmeticsTab:
    def __init__(self, save):
        self.save = save
        self.cosmetics = None
      
    def load(self):
        self.cosmetics = self.save["progress_data"]["cosmetics"]

        # Ensure golden and prismatics lists
        for skin_type in ("golden", "prismatic", "extra"):
            if skin_type not in self.cosmetics:
                self.cosmetics[skin_type] = []

        # TODO: Reset switch buttons
        # for button in ()
        # user_data=("golden", True)

        for item in items:
            golden = False
            golden_is_new = False
            index = self.get_index(item, "golden")
            if index != -1:
                golden = True
                golden_is_new = self.cosmetics["golden"][index].endswith(";new")
            
            prismatic = False
            prismatic_is_new = False
            extra = (0, 0, 0)
            index = self.get_index(item, "prismatic")
            if index != -1:
                prismatic = True
                prismatic_is_new = self.cosmetics["prismatic"][index].endswith(";new")
                
                c = self.cosmetics["extra"][index]["c"]
                extra = [int(rgb, 16) for rgb in (c[1:3], c[3:5], c[5:7])]

            dpg.configure_item(f"{item}-golden", default_value=golden)
            dpg.configure_item(f"{item}-golden-new", default_value=golden_is_new)
            dpg.configure_item(f"{item}-prismatic", default_value=prismatic)
            dpg.configure_item(f"{item}-prismatic-new", default_value=prismatic_is_new)
            dpg.configure_item(f"{item}-extra", default_value=extra)

    def open(self, _, value, group_and_item):
        if not self.cosmetics:
            return
        
        group, item = group_and_item
        index = self.get_index(item, group)

        if value and index == -1:  # Open
            self.cosmetics[group].append(f"{item};new")
            if group == "prismatic":
                self.cosmetics["extra"].append({"c": "#000000"})
                dpg.configure_item(f"{item}-extra", default_value=(0, 0, 0))
            
            dpg.configure_item(f"{item}-{group}-new", default_value=True)
            print(f"Opened {item} {group} skin")
        
        elif not value and index != -1:  # Close
            self.cosmetics[group].pop(index)
            if group == "prismatic":
                self.cosmetics["extra"].pop(index)
                # dpg.configure_item(f"{item}-new", ...)
                dpg.configure_item(f"{item}-extra", default_value=(0, 0, 0))

            dpg.configure_item(f"{item}-{group}-new", default_value=False)
            print(f"Closed {item} {group} skin")

    def open_all(self, _, app_data, group_and_value):
        if not self.cosmetics:
            return
        
        group, value = group_and_value
        for item in items:
            self.open(_, value, (group, item))
            dpg.configure_item(f"{item}-{group}", default_value=value)

        dpg.configure_item(_, user_data=(group, not value))

    def mark(self, _, value, group_and_item):
        if not self.cosmetics:
            return
        
        group, item = group_and_item
        index = self.get_index(item, group)

        if index != -1:
            # Add ";new"
            if value and not self.cosmetics[group][index].endswith(";new"):
                self.cosmetics[group][index] += ";new"
                print(f"Marked as new {item} {group} skin")

            # Remove ";new"
            if not value:
                print(f"Marked as old {item} {group} skin")
                self.cosmetics[group][index] = self.cosmetics[group][index].replace(";new", "")

    def mark_all(self, _, value, group_and_value):
        if not self.cosmetics:
            return
        
        group, value = group_and_value
        for item in items:
            self.mark(_, value, (group, item))
            dpg.configure_item(f"{item}-{group}-new", default_value=value)

        dpg.configure_item(_, user_data=(group, not value))

    def get_index(self, search_item, cosmetics_type):
        for i, item in enumerate(self.cosmetics[cosmetics_type]):
            if item.replace(";new", "") == search_item:
                return i
            
        return -1
    
    def color(self, _, value, group_and_item):
        if not self.cosmetics:
            return
        
        group, item = group_and_item
        index = self.get_index(item, group)

        if index != -1:
            r, g, b, a = [int(c * 255) for c in value]
            color = "#%02x%02x%02x" % (r, g, b)
            self.cosmetics["extra"][index]["c"] = color
            
            print(f"Changed color for {item} on {color}")

    def clear_colors(self, _):
        if not self.cosmetics:
            return
        
        group = "extra"
        value = (0, 0, 0, 0)
        for item in items:
            self.color(_, value, ("prismatic", item))
            dpg.configure_item(f"{item}-extra", default_value=value)

    def gui(self):
        with dpg.child_window(no_scrollbar=True, border=False):
            # with dpg.group(horizontal=True):
            #     with dpg.group(width=200):
            #         dpg.add_text("Позолота")

            #         dpg.add_button(label="Открыть всю")
            #         dpg.add_button(label="Закрыть всю")

            #         dpg.add_button(label="Отметить всю как новую")
            #         dpg.add_button(label="Отметить всю как старую")
            
            #     with dpg.group(width=200):
            #         dpg.add_text("Преломления")

            #         dpg.add_button(label="Открыть все")
            #         dpg.add_button(label="Закрыть все")

            #         dpg.add_button(label="Отметить все как новые")
            #         dpg.add_button(label="Отметить все как старые")
                
            #     with dpg.group(width=200):
            #         dpg.add_text("Экстра")
            #         dpg.add_button(label="Сбросить цвета")

            # dpg.add_separator()
            # dpg.add_text("Открытые облики")

            with dpg.table(tag="cosmetics_table", resizable=True, policy=dpg.mvTable_SizingStretchProp):
                dpg.add_table_column(label="Предмет")
                dpg.add_table_column(label="Позолота")
                dpg.add_table_column(label="Преломление")
                dpg.add_table_column(label="Экстра")
                
                with dpg.table_row():
                    dpg.add_text("Все предметы")

                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Открыть", tag="golden", callback=self.open_all, user_data=("golden", True))
                        dpg.add_button(label="Отметить", tag="golden-new", callback=self.mark_all, user_data=("golden", False))

                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Открыть", tag="prismatic", callback=self.open_all, user_data=("prismatic", True))
                        dpg.add_button(label="Отметить", tag="prismatic-new", callback=self.mark_all, user_data=("prismatic", False))
                    
                    dpg.add_button(label="Сбросить", tag="colors", callback=self.clear_colors)

                for item in items:
                    with dpg.table_row():
                        dpg.add_text(item)

                        with dpg.group(horizontal=True):
                            dpg.add_checkbox(label="Есть", tag=f"{item}-golden", callback=self.open, user_data=("golden", item))
                            dpg.add_checkbox(label="Новая", tag=f"{item}-golden-new", callback=self.mark, user_data=("golden", item))

                        with dpg.group(horizontal=True):
                            dpg.add_checkbox(label="Есть", tag=f"{item}-prismatic", callback=self.open, user_data=("prismatic", item))
                            dpg.add_checkbox(label="Новое", tag=f"{item}-prismatic-new", callback=self.mark, user_data=("prismatic", item))
                        
                        dpg.add_color_edit(label="Цвет", tag=f"{item}-extra", no_alpha=True, display_mode=dpg.mvColorEdit_hex, no_drag_drop=True, no_tooltip=True, no_inputs=True, callback=self.color, user_data=("prismatic", item))

