import dearpygui.dearpygui as dpg

from tools.setup import *

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

        # Dates
        for value in ("nextSpawnDate", "epicSpawnPending", "basicQuestDate"):
            dpg.configure_item(
                value,
                default_value=self.quests[value]
            )
        
        dpg.configure_item("daily_and_weekly", show=False)

        # Active quests
        dpg.delete_item("daily", children_only=True)
        if len(self.quests["active"]):
            dpg.configure_item("daily_and_weekly", show=True)
            with dpg.group(parent="daily"):
                dpg.add_text(i18n["active_quests"])
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
            dpg.configure_item("daily_and_weekly", show=True)
            with dpg.group(parent="weekly"):
                dpg.add_text(i18n["weekly_quest"])
                dpg.add_checkbox(
                    label=self.weekly["activeQuest"]["type"],
                    default_value=self.weekly["activeQuest"]["completed"],
                    callback=self.change,
                    user_data=("weekly_quest", "activeQuest", "completed")
                )

        # Events
        dpg.delete_item("events", children_only=True)
        if self.events["sIds"]:
            for sId in self.events["sIds"]:
                with dpg.group(parent="events"):
                    dpg.add_separator()
                    dpg.add_text(f"{i18n["event"]} {sId}")

                    if not "pp" in self.events[sId]:
                        self.events[sId]["pp"] = False

                    premium_prizes = self.events[sId]["pp"]

                    dpg.add_checkbox(
                        label=i18n["premium_awards"],
                        default_value=premium_prizes,
                        callback=self.change,
                        user_data=("events", sId, "pp")
                    )

                    dpg.add_input_int(
                        label=i18n["tasks_completed"],
                        default_value=self.events[sId]["rwds"]["rp"],
                        callback=self.change,
                        user_data=("events", sId, "rwds", "rp")
                    )

                    if self.events[sId]["objs"]["ids"]:
                        dpg.add_text(i18n["tasks_progress"])

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
            with dpg.group(tag="dates"):
                dpg.add_text(i18n["dates"])
                dpg.add_input_text(
                    label=i18n["basic_quest"],
                    tag="basicQuestDate",
                    callback=self.change,
                    user_data=("custom_quests", "basicQuestDate")
                )
                dpg.add_input_text(
                    label=i18n["next_legend"],
                    tag="nextSpawnDate",
                    callback=self.change,
                    user_data=("custom_quests", "nextSpawnDate")
                )
                dpg.add_checkbox(
                    label=i18n["legend_spawn_pending"],
                    tag="epicSpawnPending",
                    callback=self.change,
                    user_data=("custom_quests", "epicSpawnPending")
                )

            with dpg.group(tag="daily_and_weekly", show=False):
                dpg.add_separator()
                with dpg.table(header_row=False, resizable=True):
                    dpg.add_table_column()
                    dpg.add_table_column()
                    
                    with dpg.table_row():
                        dpg.add_group(tag="daily")
                        dpg.add_group(tag="weekly")

            dpg.add_group(tag="events")
