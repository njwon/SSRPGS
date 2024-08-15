import dearpygui.dearpygui as dpg

def loading():
    class LoadingWindow:
        def __enter__(self):
            with dpg.window(
                modal=True,
                no_title_bar=True,
                no_resize=True,
                no_move=True,
                tag="loading",
                pos=[(600 - 64) // 2, (394 - 64) // 2],
                width=64,
                height=64,
                min_size=[32, 32],
                no_background=True
            ):
                dpg.add_loading_indicator(circle_count=8)

        def __exit__(self, *_):
            dpg.delete_item("loading")
    
    return LoadingWindow()

# Green (?) block, on hover returns popup
def add_help(message, parent=0):
    last_item = dpg.last_item()
    group = dpg.add_group(horizontal=True, parent=parent)

    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))

    with dpg.tooltip(dpg.add_text("(?)", color=[0, 255, 0])):
        dpg.add_text(message)
