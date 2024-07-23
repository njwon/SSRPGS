import dearpygui.dearpygui as dpg

class CosmeticsTab:
    def __init__(self, save):
        self.save = save
        self.cosmetics = None
      
    def load(self):
        self.cosmetics = self.save["progress_data"]["cosmetics"]
        
        with dpg.table(parent="cosmetics_table", resizable=True, policy=dpg.mvTable_SizingStretchProp,):
            dpg.add_table_column(label="Предмет")
            dpg.add_table_column(label="Позолота")
            # dpg.add_table_column(label="Новая")
            dpg.add_table_column(label="Призматика")
            # dpg.add_table_column(label="Новая")
            # dpg.add_table_column(label="Цвет")
            
            for skin in self.cosmetics["golden"]:
                with dpg.table_row():
                    for column in range(6):
                        dpg.add_text(skin)
                        with dpg.table_cell():
                            with dpg.group(horizontal=True):
                                dpg.add_checkbox(label="Есть")
                                dpg.add_checkbox(label="Новая")
                    # with dpg.group(horizontal=True, parent="cosmetics"):
                        with dpg.table_cell():
                            with dpg.group(horizontal=True):
                                dpg.add_checkbox(label="Есть")
                                dpg.add_checkbox(label="Новая")
                                dpg.add_color_edit(no_alpha=True, display_mode=dpg.mvColorEdit_hex, no_tooltip=True, no_inputs=True)

        # for skin in self.cosmetics["golden"]:
        #     print(skin)

        #     # dpg.add_separator(parent="cosmetics")
        #     # with dpg.group(horizontal=True, parent="cosmetics"):
        #     dpg.add_checkbox(label="Позолота")
        #     dpg.add_checkbox(label="!")
        # # with dpg.group(horizontal=True, parent="cosmetics"):
        #     dpg.add_checkbox(label="Призматика")
        #     dpg.add_checkbox(label="!")
        #     dpg.add_color_edit(label="Цвет", no_alpha=True, display_mode=dpg.mvColorEdit_hex, no_tooltip=True, no_inputs=True)
        #     dpg.add_text(skin)

    def gui(self):
        with dpg.child_window(tag="cosmetics", no_scrollbar=True, border=False):
            dpg.add_group(tag="cosmetics_table")

            dpg.add_separator()
            dpg.add_text("Настройки позолоты")
            dpg.add_button(label="Открыть всю")
            dpg.add_button(label="Закрыть всю")
            dpg.add_button(label="Отметить всю")
            
            dpg.add_separator()
            dpg.add_text("Настройки призматики")
            dpg.add_button(label="Открыть всю")
            dpg.add_button(label="Закрыть всю")
            dpg.add_button(label="Отметить всю")
            dpg.add_button(label="Сбросить цвета")
