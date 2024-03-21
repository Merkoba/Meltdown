### A Python program to interface with `llama.cpp`

<img src="media/image.jpg" width="380">

---

![](https://i.imgur.com/IWlH7Ss.jpg)

### Compact Mode:

![](https://i.imgur.com/4paAA7B.jpg)

### Markdown Support:

![](https://i.imgur.com/i9eJ9OJ.jpg)

### Light Theme:

![](https://i.imgur.com/nUzsEVu.jpg)

---

## Features

Load models from your file system (only tested with gguf for now).

Stream responses in real time.

All the available configurations are what you can see in the screenshots.

All fields have context menus to perform some actions.

Recent text inputs get saved and you can access them with the context menus.

Cycle through input history to avoid typing things again.

Save logs of the conversations.

Config changes get remembered.

Save and load config files.

Prepend and append text automatically to your prompts.

Show system CPU, RAM, and temperature. Click to open `btop` etc.

Multiple chat formats available like `chatml`, `alpaca`, `vicuna`, `llama-2`, etc.

Multiple tabs, each with their own context.

Sessions are remembered, can also be saved and loaded from files.

Context menus that are filterable and respond to keyboard.

Keyboard and mouse shortcuts.

GUI completely based on Python's `Tkinter`, no big dependencies.

Installable through `pipx` with a single command.

Should be cross-platform, but only tested on Linux for now.

Several custom widgets made specifically for this program.

Starts instantly and only loads the models and conversations when needed.

Comands like `/clear`, `/stop`, `/log`, etc.

Change the font size of the output.

The conversation tabs can be re-ordered by dragging.

Buttons change color to reflect program state.

Autocomplete commands with Tab.

Scrollable config panel to pack more configs.

Close single tabs, all tabs, or old tabs.

Horizontally-scrollable snippet text areas to show code.

Custom keyboard system.

Markdown for triple backticks and single backticks.

Markdown for bold and italic.

URL highlighting and handling.

Explain words, selections, highlights.

Search for words on a search engine.

Programming language syntax highlighting.

Dark and light themes.

---

## GUI Toolkit

Python comes bundled with the `Tkinter` library which is a wrapper around `Tcl`.

This should just work after installing Python normally.

Which means Meltdown is able to run in many environments.

---

## Installation

You can install it with [pipx](https://pypi.org/project/pipx/):

```sh
pipx install git+https://github.com/Merkoba/Meltdown --force
```

Which provides the `meltdown` command.

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

---

## Arguments

These are flags you can use when running the program.

For example: `meltdown --no-tooltips --width 800 --height 900`

---

>width

Start the window with this width.

---

>height

Start the window with this height.

---

>no-tooltips

Don't show tooltips when hovering over items.

---

>no-scrollbars

Don't display the scrollbars.

---

>no-colors

Don't display colors on the user names.

---

>no-avatars

Don't display user avatars.

---

>no-keyboard

Disable keyboard shortcuts.

---

>no-monitors

Don't show the system monitors like CPU.

---

>no-monitor-colors

Don't use colors on the system monitors.

---

>no-cpu

Don't show the CPU monitor.

---

>no-ram

Don't show the RAM monitor.

---

>no-temp

Don't show the temperature monitor.

---

>maximized

Start the window maximized.

Aliases: `--maximize` and `--max`

>compact

Start in compact mode.

---

>theme

Change the color theme of the whole program.

Either `dark` or `light`.

---

>test

Open a test tab for debugging.

---

>version

Show the version of the program.