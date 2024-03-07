### A Python program to interface with `llama.cpp`

<img src="media/image.jpg" width="380">

![](https://i.imgur.com/QOxzDEE.jpg)

---

## Features

Load models from your file system (Only tested with gguf for now).

All the available configurations are what you can see in the screenshot.

All fields have context menus to perform some actions.

Recent text inputs get saved and you can access them with the context menu.

Cycle through input history to avoid typing things again.

Save logs of the conversations.

Config changes get remembered.

Save and load config files.

Prepend and append text automatically to your prompt.

Show system CPU and RAM usage.

---

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

You will need some models to play with.

Here's some small ones you can use:

https://huggingface.co/TheBloke/Pirouette-7B-GGUF

https://huggingface.co/TheBloke/phi-2-GGUF

You can find more in that site.