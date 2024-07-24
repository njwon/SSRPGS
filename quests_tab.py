import dearpygui.dearpygui as dpg

class QuestsTab:
    def __init__(self, save):
        self.save = save
      
    def load(self):
        pass

    def gui(self):
        dpg.add_text("Открытые места")
