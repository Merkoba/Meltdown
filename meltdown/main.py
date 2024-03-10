# Modules
from .app import app
from .widgets import widgets
from .model import model
from .sessions import sessions
from . import state
from . import system


def main() -> None:
    state.load_files()
    sessions.load()
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
