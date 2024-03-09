# Modules
from .app import app
from .widgets import widgets
from .model import model
from . import state
from . import system


def main() -> None:
    state.load_files()
    widgets.setup()
    system.start()
    app.setup()

    try:
        app.run()
    except KeyboardInterrupt:
        pass

    try:
        model.unload()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
