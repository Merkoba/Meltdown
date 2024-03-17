# Modules
from .app import app
from .widgets import widgets
from .model import model
from .session import session
from .args import args
from .commands import commands
from .keyboard import keyboard
from . import state
from . import system


def main() -> None:
    args.parse()
    state.load_files()
    session.load()
    widgets.setup()
    keyboard.setup()
    commands.setup()
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
