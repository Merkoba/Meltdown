## Arguments

These are flags you can use when running the program.

For example: `meltdown --no-tooltips --width 800 --height 900`

There are some keywords you can use.

These are replaced in the argument:

>@now

This is replaced with the current unix time in seconds.

You might want to use this when saving files.

For example `/saveconfig @now` might save `1712344148.json`.

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

>maximized

Start the window maximized.

Alias: `--max`

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

Default: 0.15

Delay in seconds between each print when streaming.

For example `--delay 0.25` would print more frequently compared to `--delay 1.0`.

This might be useful if you don't want to overwhelm the interface with very frequent prints.

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