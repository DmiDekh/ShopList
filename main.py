from core import Core 
from GUI.gui_flet.app import App




if __name__ == "__main__":
    core = Core()
    app = App(core)
    app.run()