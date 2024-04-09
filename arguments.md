## Arguments

These are flags you can use when running the program.

For example: `meltdown --no-tooltips --width 800 --height 900`

This is how the program is configured. There is no settings window.

Except configs that tweak the model/stream. Those are in the interface.

---

There are some keywords you can use in the command arguments:

>@now

This is replaced with the current unix time in seconds.

You might want to use this when saving files.

For example `/saveconfig @now` might save `1712344148.json`.

---

>alias

You can define one or more command aliases.

The name of the alias is at the start and the value is after `=`.

For example:

```sh
--alias "grab = /tab 1 & /select" --alias "destroy = /close force"
```

Or maybe a prompt alias:

```sh
--alias "history = /input what happened on this day?"
```

---

>task

You can run automated tasks.

The format is [seconds] [commands] [/now (optional)]

For example:

```sh
--task "30 /tab 1 & /input hello world /now"
```

This will go to the first tab and then prompt the model with "hello world".

It will run the first task instantly and then wait 30 seconds for the next iteration.

You can define multiple tasks like this.

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

>no-taps

Disable double ctrl taps.

---

>no-system

Don't show the system monitors like CPU.

---

>no-system-colors

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

>no-wrap

Disable wrapping when selecting items.

---

>no-tabs

Don't show the tab bar.

---

>no-stream

Show responses once they're ready instead of streaming live.

---

>no-empty

Don't save empty conversations.

---

>maximize

Start the window maximized.

---

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

---

>config

Load a config file.

This can be a name, you can omit the `.json`.

It can also be a direct path.

---

>session

Load a session file.

This can be a name, you can omit the `.json`.

It can also be a direct path.

---

>on-log

This is a command to run after saving a log file.

For example you can use `--on-log geany` to automatically

open the file on the Geany text editor after it is saved.

It simply passes the file path as an argument to the command/script.

---

>numbers

Show numbers in the tab bar.

---

>max-tabs

Max number of tabs to keep. The older ones are closed automatically.

Unlimited by default.

---

>f1 to f12

You can assign commands to every function key.

For example `--f1 "/tab 1"` or `--f11 "/fullscreen & /sleep 1 & /about"`.

Check /commands to see all available commands.

Some of them have default commands but they can be overridden.

---

>input

Use this input automatically at startup.

It will load and ask the model automatically.

Commands are also supported.

It simulates a normal input submit.

This can also be piped:

```sh
echo "hello world" | meltdown
```

This can also be used without the flag:

```sh
meltdown "hello world"
```

---

>force

Allow opening multiple instances.

---

>alt-palette

Show the commands instead of the descriptions in the command palette.

---

>no-bottom

Don't show the Go To Bottom bar.

---

>no-bottom-autohide

Don't autohide the Go To Bottom bar.

Always reserve the space.

Instead it just disables it.

---

>old-tabs-minutes

Default: 30

Consider tabs old after these minutes.

---

>max_list_items

Default: 10

Max number to keep in lists.

Like the Recent items when you right click the Input.

---

>list-item-width

Default: 100

How many characters the list items can have.

---

>max-tab-width

Max number of characters to show in tab names.

---

>system-threshold

Default: 70

Show system monitors as critical after this % threshold.

---

>system-delay

Default: 3

Delay in seconds for system monitor updates.

---

>drag-threshold

Default: 88

This controls re-ordering tabs when dragging with the mouse.

This is the amount of pixels that must be traveled by the mouse.

The higher the number the less sensitive the tab dragging will be.

---

>no-tab-highlight

Don't highlight the tab when streaming.

---

>quiet

Don't show some messages.

---

>delay

Default: 0.1

Delay in seconds between each print when streaming.

For example `--delay 0.25` would print more frequently compared to `--delay 1`.

This might be useful if you don't want to overwhelm the interface with very frequent prints.

Use `0` to not have a delay at all.

---

>prefix

Default: "/"

The command prefix for all commands.

Like `/` in `/about`

---

>andchar

Default: "&"

The command used to join commands.

Like `&` in `/tab 1 & /select`

---

>keychar

Default: "@"

Character to use for keywords like `@date`.

---

>no-commands

Disable commands when submitting the input.

Treat all text as the prompt, don't check for commands.

---

>compact-model

>compact-system

>compact-details

>compact-buttons

>compact-addons

>compact-input

If any of these are set, compact mode will be customized.

If customized, it will compact/hide exactly what you defined.

Else it hides by default: system, details, and addons.

For example: `--compact-model --compact buttons`

In compact mode only the model frame and the buttons frame will be hidden.

---

>display

Activate display mode.

This hides all frames except the display and tabs.

Input submit is also disabled.

Commands and keyboard shortcuts still work.

---

>no-intro

Don't print the intro in conversations.

---

>autorun

A command or chain of commands to run at startup automatically.

---

>no-terminal

Don't enable the terminal to input prompts and commands.

---

>terminal-height

Default: 3

Reserve these number of lines for the prompt.

There is an autocomplete menu that needs some lines to be displayed.

---

>terminal-vi

Enable vi mode on the terminal.

---

>no-terminal-memory

Don't remember words when using the terminal.

These are added to the autocomplete list.

---

>terminal-memory-min

Default: 4

Minimum number of characters words need to have to be remembered in the terminal.

---

>autocomplete-memory-min

Default: 4

Minimum number of characters words need to have to be remembered in the input.

---

>listener

Enable the input listener.

This reads a file located in a temp directory.

The file is called `mlt_meltdown.input`.

In Linux it would be located inside `/tmp`

This file is read, and if it has content it used for the input.

The file is then emptied.

So for instance you can trigger an input by doing this:

`echo "hello world" > /tmp/mlt_meltdown.input`

---

>listener-delay

Default: 0.5

Delay in seconds for the listener loop check.

If this is lower than 0.1 the listener won't start.

---

>on-top

Make the window always on top.

This means clicking outside the window won't hide it.

---

>monospace

Use monospace font for the output.

---

>commandoc

Make the commandoc and save it on this path.

This is meant for the developer to make the documentation.

---

>afterstream

Execute this command after streaming a response.

For example:

```sh
--after-stream "/logjson & /exit 3" "What is math?"
```

It will use `What is math?` as the prompt automatically.

After it's done, it will save the conversation to a JSON file and exit in 3 seconds.

---

>no-clean-slate

Don't make a new tab when starting with an input.

By default when you start the program with an input

it will smartly check if it should re-use an empty tab or make a new one.

If you disable this, it will always use the last tab even if not empty.

---

>tabs-always

Always show the tab bar even if only one tab is open.

Else it will auto-hide the tab bar when only 1 tab.

And show the tab bar when more tabs are opened.

---

>no-model-icon

Don't show the model icon.

This is the icon on the top right that reflect model status.

---

>no-more-button

Don't show the More button at the right of the buttons frame.

---

>no-model-feedback

Don't show feedback when the model is loading.

---

>time

Show the loading time at startup.

---

>verbose

Output messages from llama.cpp when streaming.

---

>no-emojis

Don't use emojis on messages or the interface.