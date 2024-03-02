# Modules
from config import config
from model import model
import frames


def main() -> None:
    config.prepare(__file__)
    frames.frame_model()
    frames.frame_settings()
    frames.frame_system()
    frames.frame_output()
    frames.frame_input()
    frames.setup()
    config.app.mainloop()
    model.check_thread()


if __name__ == "__main__":
    main()
