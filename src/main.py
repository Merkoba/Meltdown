# Modules
from config import config
from model import model
import frames
import timeutils


def main() -> None:
    now = timeutils.now()
    config.prepare(__file__)
    frames.frame_model()
    frames.frame_settings()
    frames.frame_system()
    frames.frame_output()
    frames.frame_input()
    frames.setup()
    # model.load()
    print(timeutils.check_time("Started", now)[0])
    config.app.mainloop()


if __name__ == "__main__":
    main()
