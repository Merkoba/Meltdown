# Modules
from config import config
from model import model
import frames
import actions
import state


def main() -> None:
    state.load_config_file()
    state.load_models_file()
    frames.frame_model()
    frames.frame_settings()
    frames.frame_system()
    frames.frame_output()
    frames.frame_input()
    frames.setup()
    actions.intro()
    config.app.mainloop()
    model.check_thread()


if __name__ == "__main__":
    main()
