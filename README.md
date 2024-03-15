### A Python program to interface with `llama.cpp`

<img src="media/image.jpg" width="380">

![](https://i.imgur.com/jqw6tut.jpg)

Compact Mode:

![](https://i.imgur.com/RQh9bQL.jpg)

---

## Features

Load models from your file system (Only tested with gguf for now).

Stream response tokens as they appear.

All the available configurations are what you can see in the screenshot.

All fields have context menus to perform some actions.

Recent text inputs get saved and you can access them with the context menus.

Cycle through input history to avoid typing things again.

Save logs of the conversations.

Config changes get remembered.

Save and load config files.

Prepend and append text automatically to your prompts.

Show system CPU, RAM, and temperature. Click to open `htop` etc.

Multiple chat formats available like `chatml`, `alpaca`, `vicuna`, `llama-2`, etc.

Multiple tabs, each with their own context.

Sessions are remembered, can also be saved and loaded from files.

Context menus that are filterable and respond to keyboard.

Keyboard and mouse shortcuts.

GUI completely based on Python's `Tkinter`, no big dependencies.

Installable through `pipx` with a single command.

Should be cross-platform, but only tested on linux for now.

Several custom widgets made specifically for this program.

Starts instantly and only loads the model and conversations when needed.

Comands like `/clear`, `/stop`, `/log`, etc.

Change the font size of the output.

Slider rows to accomodate more config widgets.

The conversation tabs can be re-ordered by dragging.

---

## Installation

You might be able to install it with `pipx`:

```sh
pipx install git+https://github.com/madprops/meltdown --force
```

Which should provide the `meltdown` command.

---

To install manually use a virtual env and `requirements.txt`.

You can use `scripts/venv.sh` to automate this.

To run it use `run.sh` in the root dir.

---

## Models

You will need some models to play with.

Here's a small one you can use:

https://huggingface.co/TheBloke/dolphin-2_6-phi-2-GGUF

You can find more in that site.