import dearpygui.dearpygui as dpg

class TimesTab:
    def __init__(self, save):
        self.save = save

    def load(self):
        dpg.configure_item("nextTreasureAvailableDate", default_value=self.save["progress_data"]["crypt_intro"]["nextTreasureAvailableDate"])
        dpg.configure_item("skullnata", default_value=self.save["progress_data"]["quest_data"]["skullnata"])  # THIS VALUE DOES NOT EVEN MATTER ANY THING!

    def change(self, _, value, path):
        head = self.save
        for key in path[:-1]:
            head = head[key]

        head[path[-1]] = value

        print(f"Changed field: {path[-1]}: {head[path[-1]]}")

    def gui(self):
        with dpg.child_window(
            no_scrollbar=True,
            border=False
        ):
            dpg.add_text("Врата")
            dpg.add_input_text(
                label="Таймаут сокровища",
                tag="nextTreasureAvailableDate",
                width=230,
                callback=self.change,
                user_data=("progress_data", "crypt_intro", "nextTreasureAvailableDate")
            )
            dpg.add_input_text(
                label="Черепушка-пиньята",
                tag="skullnata",
                width=230,
                callback=self.change,
                user_data=("progress_data", "quest_data", "skullnata")
            )
            
            dpg.add_separator()
            dpg.add_text("Фабрика сокровищ")
            dpg.add_input_text(
                label="Уникальная дата",
                width=230
            )
            dpg.add_input_text(
                label="Дата кристаллов",
                width=230
            )
            dpg.add_input_text(
                label="Дата золота",
                width=230
            )
            
            dpg.add_separator()
            dpg.add_text("Квесты")
            dpg.add_input_text(
                label="Следующий легендарный квест",
                width=230
            )
            dpg.add_input_text(
                label="Следующий базовый квест",
                width=230
            )
            dpg.add_input_text(
                label="Таймаут еженедельного квеста",
                width=230
            )
            dpg.add_button(
                label="Сбросить кулдауны всех легенд"
            )

# time regex
# \d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}