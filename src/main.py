# Modules
from config import config
from widgets import widgets
from model import model
import state


def main() -> None:
    state.load_config_file()
    state.load_models_file()
    widgets.setup()
    widgets.intro()
    config.app.mainloop()
    model.check_thread()


if __name__ == "__main__":
    main()
