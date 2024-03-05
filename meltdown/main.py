# Modules
from .app import app
from .widgets import widgets
from .model import model
from . import state


def main() -> None:
    state.load_files()
    widgets.setup()
    widgets.intro()
    app.run()
    model.stop_stream()


if __name__ == "__main__":
    main()
