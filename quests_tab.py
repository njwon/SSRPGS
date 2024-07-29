import dearpygui.dearpygui as dpg

class QuestsTab:
    def __init__(self, save):
        self.save = save
        self.events = None
        self.quests = None
        self.weekly = None

    def change(self, _, value, path):
        # Pointer on last object inside of a dict
        head = self.save["progress_data"]
        for key in path[:-1]:
            head = head[key]

        head[path[-1]] = value

        print(f"Changed field: {path[-1]}: {head[path[-1]]}")
      
    def load(self):
        self.events = self.save["progress_data"]["events"]
        self.quests = self.save["progress_data"]["custom_quests"]
        self.weekly = self.save["progress_data"]["weekly_quest"]

        # Daily quests
        dpg.delete_item("daily", children_only=True)
        with dpg.group(parent="daily"):
            for i, quest in enumerate(self.quests["active"]):
                if "completed" not in quest:
                    quest["completed"] = False
                
                dpg.add_checkbox(
                    label=f"{quest["customQuestId"]}",
                    default_value=quest["completed"],
                    callback=self.change,
                    user_data=("custom_quests", "active", i, "completed")
                )

        # Weekly
        dpg.delete_item("weekly", children_only=True)
        if "activeQuest" in self.weekly:
            with dpg.group(parent="weekly"):
                dpg.add_checkbox(
                    label=self.weekly["activeQuest"]["type"],
                    default_value=self.weekly["activeQuest"]["completed"],
                    callback=self.change,
                    user_data=("weekly_quest", "activeQuest", "completed")
                )
            
        # Events
        dpg.delete_item("events", children_only=True)
        for sId in self.events["sIds"]:
            with dpg.group(parent="events"):
                dpg.add_separator()
                dpg.add_text(f"Событие {sId}")

                if not "pp" in self.events[sId]:
                    self.events[sId]["pp"] = False

                premium_prizes = self.events[sId]["pp"]

                dpg.add_checkbox(
                    label="Премиум-награды",
                    default_value=premium_prizes,
                    callback=self.change,
                    user_data=("events", sId, "pp")
                )

                dpg.add_input_int(
                    label="Целей завершено",
                    default_value=self.events[sId]["rwds"]["rp"],
                    callback=self.change,
                    user_data=("events", sId, "rwds", "rp")
                )

                if self.events[sId]["objs"]["ids"]:
                    dpg.add_text("Прогресс целей")

                    for task_id in self.events[sId]["objs"]["ids"]:
                        task_progress = 0

                        # Check task progress and zero it if not exists
                        if task_id in self.events[sId]["objs"]:
                            if "p" in self.events[sId]["objs"][task_id]:
                                task_progress = self.events[sId]["objs"][task_id]["p"]
                            else:
                                self.events[sId]["objs"][task_id]["p"] = 0
                        else:
                            self.events[sId]["objs"][task_id] = {"p": 0}
                        
                        dpg.add_input_int(
                            label=task_id,
                            default_value=task_progress,
                            callback=self.change,
                            user_data=("events", sId, "objs", task_id, "p")
                        )

    def gui(self):
        with dpg.child_window(border=False, no_scrollbar=True):
            dpg.add_text("Ежедневные квесты")
            dpg.add_group(tag="daily")

            dpg.add_separator()
            dpg.add_text("Еженедельный квест")
            dpg.add_group(tag="weekly")

            dpg.add_group(tag="events")
