# Modules
from .inputcontrol import inputcontrol
from .args import args

# Standard
import threading


def get_input() -> None:
    while True:
        user_input = input("Input: ")
        inputcontrol.submit(text=user_input)


def start() -> None:
    if not args.terminal:
        return

    thread = threading.Thread(target=get_input, args=())
    thread.daemon = True
    thread.start()
