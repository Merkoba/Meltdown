# Modules
from .app import app
from .widgets import widgets
from .display import display
from .model import model
from .session import session
from .args import args
from .commands import commands
from .keyboard import keyboard
from . import filemanager
from . import system


def main() -> None:
    args.parse()
    filemanager.load()
    app.prepare()
    widgets.make()
    model.setup()
    display.make()
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
