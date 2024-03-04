### A Python program to interface with `llama.cpp`

<img src="media/image.jpg" width="380">

![](https://i.imgur.com/wFolNJH.jpg)

You will first need to have [llama.cpp](https://github.com/ggerganov/llama.cpp) compiled and installed.

---

You might be able to install meltdown with `pipx`:

```sh
pipx install git+https://github.com/madprops/meltdown
```

Which should provide the `meltdown` command.

---

To install manually use a virtual env and `requirements.txt`.

You can use `scripts/venv.sh` to automate this.

To run it use `run.sh` in the root dir.