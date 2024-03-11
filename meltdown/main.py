# Modules
from .app import app
from .widgets import widgets
from .model import model
from .session import session
from .menus import Menu
from . import state
from . import system


def main() -> None:
    state.load_files()
    session.load()
    widgets.setup()
    system.start()
    app.setup()
    Menu.setup()

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
