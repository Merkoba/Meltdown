# Modules
from meltdown.app import app
from meltdown.widgets import widgets
from meltdown.model import model
from meltdown import state


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
