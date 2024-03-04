# Modules
from app import app
from widgets import widgets
from model import model
import state


def main() -> None:
    state.load_config_file()
    state.load_models_file()
    state.load_inputs_file()
    widgets.setup()
    widgets.intro()
    app.run()
    model.stop_stream()


if __name__ == "__main__":
    main()
