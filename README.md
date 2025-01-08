## An interface for llama.cpp, ChatGPT, and Gemini

<img src="meltdown/image.jpg" width="380">

---

## Index
1. [Screenshots](#screenshots)
1. [Models](#models)
1. [ChatGPT](#chatgpt)
1. [Gemini](#gemini)
1. [Installation](#installation)
1. [Console](#console)
1. [Listener](#listener)
1. [Upload](#upload)
1. [Signals](#signals)
1. [Images](#images)
1. [Keywords](#keywords)
1. [Commands](commands.md)
1. [Arguments](arguments.md)
1. [Keyboard](keyboard.md)

---

## Screenshots <a name="screenshots"></a>

![](img/readme_1.png)

![](img/readme_2.png)

![](img/readme_3.png)

---


## Installation <a name="installation"></a>

Note: By default `llama.cpp` (local model) support is not installed.

Read below to learn how to enable it.

Also, this has only been tested on `Linux`.

---

### Using pipx

You can install it with [pipx](https://pypi.org/project/pipx/):

```sh
pipx install git+https://github.com/Merkoba/Meltdown
```

That will only enable remote features like `ChatGPT` and `Gemini`.

But that means the installation is easier and faster.

---

If you want to enable `llama.cpp` support for local models do this:

```sh
pipx install git+https://github.com/Merkoba/Meltdown#egg=meltdown[llama]
```

The difference is `#egg=meltdown[llama]` added at the end.

---

To install it with `Vulkan` support (GPU), you can do this:

```sh
CMAKE_ARGS="-DGGML_VULKAN=on" pipx install git+https://github.com/Merkoba/Meltdown#egg=meltdown[llama]
```

---

Intalling with `pipx` provides the `meltdown` command.

And if on `Linux`, you should now have a `.desktop` entry to launch it.

You can uninstall it with `pipx uninstall meltdown`.

---

### Manual Installation

To install manually, use a virtual env and `requirements.txt`.

You can use `scripts/venv.sh` to automate this.

---

To add local model support run `scripts/venv_llama.sh`.

There's a `scripts/venv_llama_amd.sh` to install with `Vulkan` support for `AMD`.

Pick one of those for local model support.

The `llama.cpp` library is defined in `llama_reqs.txt`.

These should be called after running `venv.sh` as they only add extra libraries.

---

To run the program, use `run.sh` in the root dir.

---

Read more about [`llama-cpp-python`](https://github.com/abetlen/llama-cpp-python).

This is the library used to interface with `llama.cpp`.

It is responsible for compiling `llama.cpp`.

---

## Models <a name="models"></a>

Local `gguf` models can be used.

Here's a good one you can use:

https://huggingface.co/QuantFactory/Meta-Llama-3-8B-Instruct-GGUF/blob/main/Meta-Llama-3-8B-Instruct.Q5_K_M.gguf

You can find more on that site.

The bigger the model, the longer it will take to load.

---

## ChatGPT <a name="chatgpt"></a>

ChatGPT is also supported.

You must first set the API key for it to work.

This can be done using the model menu: `Set OpenAI Key`.

Or using the `openaikey` command.

Then pick the model you want: `Use GPT Model`.

---

## Gemini <a name="gemini"></a>

Gemini is also supported.

You must first set the API key for it to work.

This can be done using the model menu: `Set Google Key`.

Or using the `googlekey` command.

Then pick the model you want: `Use Gemini Model`.

---

## Console <a name="console"></a>

To enable the console use `--console`.

This allows you to send actions from the terminal that launched the program.

You can enter a simple text prompt, or send a command if the command prefix is used.

It uses `prompt_toolkit` and it shows autocomplete suggestions with recently used words, or commands.

You could have the main program displayed on a monitor and control it with the terminal in another monitor for instance.

The console is not enabled by default because it can be problematic on certain environments depending on how the program was launched (i.e High CPU usage).
But it should work well on normal terminal launches.

![](img/console.jpg)

![](img/console_2.jpg)

---

## Listener <a name="listener"></a>

There's a listener mode that can be enabled with `--listener`.

When the listener is active, it will periodically read a file and check for changes.

If it finds text, it will use it as the prompt, or as a command if it starts with the command prefix.

It will then empty the file after using it.

You can do for instance `echo "hello" > /tmp/mlt_meltdown.input`.

Or: `echo "/new" > /tmp/mlt_meltdown.input`.

By default it checks `/tmp/mlt_meltdown.input` if on Linux.

Temp Dir + `mlt_meltdown.input`.

But the file path can also be set with `--listener-path`.

This is another way to control the program remotely.

![](img/listener.jpg)

---

## Upload  <a name="upload"></a>

Conversations can be uploaded to a text hosting service.

For now it works with `rentry.org`.

The password (edit code) can be configured through `--upload-password`.

If no password is set, a random short word is used.

After the text is uploaded, a message appears that allows you to copy the URL.

The URL and password are also printed in the conversation window.

All the conversation can be uploaded, or just the last item.

![](img/upload.jpg)

---

## Signals <a name="signals"></a>

There is a signals system that allows to make requests to remote servers.

To use this a json file must be created and pointed to with the `---signals-file` argument.

---

Multiple signals can be defined. This is a demo with all the available keys:

```json
{
    "test": {
        "url": "https://test.com/submit",
        "method": "POST",
        "format": "text",
        "items": "all",
        "content_key": "status",
        "content_length": 500,
        "single_line": true,
        "data": {
            "username": "melt",
            "key": "someAuthKey"
        }
    }
}
```

---

`url` and `content_key` are always required, the rest are optional.

---

`url` is the url to use for the request. (required)

`method` can be `post`, `get`, or `put`.

`format` can be `text`, `json`, or `markdown`.

`items` can be `all`, to include the full conversation. Or `last`, to include only the last item.

`content_key` is used for the conversation text. (required)

`content_length` limits the content to that amount of characters.

`single_line` sends the content as a single line.

`data` all the data keys needed to be sent.

---

## Images <a name="images"></a>

Multi-modal models like llava 1.5 can be used.

Download the model gguf and the mmproj gguf (clip model):

https://huggingface.co/mys/ggml_llava-v1.5-7b/tree/main

Put those 2 files in the same directory.

Rename the clip model file to `mmproj.gguf`.

Set `Mode` to `images`.

Now you can use the `File` field to include a URL or path to an image.

And you can use the input to include text as normal.

While this has been tested to work, it's still considered experimental.

---

## Keywords <a name="keywords"></a>

There are some keywords you can use in commands:

---

### ((name_user))

Name of the user.

---

### ((name_ai))

Name of the AI.

---

### ((date))

Current date.

---

### ((now))

Current unix time in seconds.

---

### ((name))

Name of the current tab.

---

### ((noun))

Random noun.

---

### %@sometext%@

This is a special syntax to create `uselinks`.

These are used to prompt directly on click.