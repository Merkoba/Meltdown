## An interface for llama.cpp and ChatGPT

<img src="meltdown/image.jpg" width="380">

---

## Index
1. [Screenshots](#screenshots)
1. [Features](#features)
1. [Toolkit](#toolkit)
1. [Models](#models)
1. [ChatGPT](#chatgpt)
1. [Installation](#installation)
1. [Commands](commands.md)
1. [Arguments](arguments.md)

---

Screenshots <a name="screenshots"></a>

![](https://i.imgur.com/IWlH7Ss.jpg)

### Compact Mode:

![](https://i.imgur.com/4paAA7B.jpg)

### Markdown Support:

![](https://i.imgur.com/i9eJ9OJ.jpg)

### Light Theme:

![](https://i.imgur.com/nUzsEVu.jpg)

---

## Features <a name="features"></a>

Load models from your file system (only tested with gguf for now).

Or use ChatGPT with your personal api key.

Stream responses in real time.

Various configs to tweak the responses like `seed`, `max_tokens`, `top_p`, `top_k`, `temperature`.

Configs to tweak llama.cpp like the number of threads to use or mem-lock.

Context is saved to use on future prompts, optionally.

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

Close single tabs, all tabs, old tabs, to the left, to the right, or others.

Horizontally-scrollable snippet text areas to show code.

Custom keyboard system.

Markdown for triple backticks and single backticks.

Markdown for bold and italic.

URL highlighting and handling.

Explain words, selections, highlights.

Search for words on a search engine.

Programming language syntax highlighting.

Dark and light themes.

Command similarity check ( >= 0.8 ).

Load config and session files.

Click and double click words.

Start new conversations based on some words.

Perform commands automatically upong saving log files.

Tab list with filterable menu.

Find text, case sensitive and insensitive.

Find word-bound text or use regex.

Dialog buttons that respond to keyboard.

View text and view json raw modes.

Find across all open tabs.

Select tabs with keyboard numbers.

Command palette with recent usage remembered.

Double ctrl tap (to open the palette).

Run a program upon saving a log.

Save logs of all conversations at once.

Can be started with a prompt to use automatically.

Text can be piped to the program as the input.

Create up to 3 tasks to run commands periodically automatically.

Create command aliases that run other commands.

Send prompt input and commands through the terminal.

Over 70 commands and 80 arguments.

Powerful input line prompt for the terminal, with autocomplete, memory, and vi mode.

Optional listener that checks a file periodically to use as input.

And more.

---

## GUI Toolkit <a name="toolkit"></a>

Python comes bundled with the `tkinter` library which is a wrapper around `Tcl`.

This should just-work after installing Python normally.

It should work in different operating systems (cross-platform).

It doesn't depend on a browser engine or a proprietary toolkit.

This means Meltdown is able to run in many environments in a lightweight manner.

(Only tested on Linux for now)

---

## Models <a name="models"></a>

You will need some models to play with.

Here's a small one you can use:

https://huggingface.co/TheBloke/dolphin-2_6-phi-2-GGUF

You can find more in that site.

---

## ChatGPT <a name="chatgpt"></a>

ChatGPT is also supported.

You must first set the API key for it to work.

This can be done using the main menu: `Set API Key`.

Then pick the model you want: `Use GPT Model`.

---

## Installation <a name="installation"></a>

You can install it with [pipx](https://pypi.org/project/pipx/):

```sh
pipx install git+https://github.com/Merkoba/Meltdown --force
```

Which provides the `meltdown` command.

---

To install manually use a virtual env and `requirements.txt`.

You can use `scripts/venv.sh` to automate this.

To run it use `run.sh` in the root dir.