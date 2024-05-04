## Arguments

Here are all the available command line arguments:

---

### version

Check the version of the program

Action: version

---

### no_tooltips

Don't show tooltips

Action: store_false

---

### no_scrollbars

Don't show scrollbars

Action: store_false

---

### no_colors

Don't show user colors

Action: store_false

---

### no_avatars

Don't show user avatars

Action: store_false

---

### no_system

Don't show system monitors

Action: store_false

---

### no_system_colors

Disable system monitor colors

Action: store_false

---

### no_cpu

Don't show the CPU monitor

Action: store_false

---

### no_gpu

Don't show the GPU monitor

Action: store_false

---

### no_gpu_ram

Don't show the GPU memory monitor

Action: store_false

---

### no_gpu_temp

Don't show the GPU temperature monitor

Action: store_false

---

### no_ram

Don't show the RAM monitor

Action: store_false

---

### no_temp

Don't show the temperature monitor

Action: store_false

---

### no_keyboard

Disable keyboard shortcuts

Action: store_false

---

### no_taps

Disable double ctrl taps

Action: store_false

---

### no_wrap

Disable wrapping when selecting items

Action: store_false

---

### no_tabs

Don't show the tab bar

Action: store_false

---

### no_stream

Don't stream responses

Action: store_false

---

### no_empty

Don't save empty conversations

Action: store_false

---

### no_bottom

Don't show the Bottom button

Action: store_false

---

### no_bottom_autohide

Don't autohide the Bottom button

Action: store_false

---

### no_reorder

Disable tab reordering by dragging

Action: store_false

---

### no_tab_highlight

Don't highlight the tab when streaming

Action: store_false

---

### no_commands

Disable commands when typing on the input

Action: store_false

---

### no_intro

Don't print the intro in conversations

Action: store_false

---

### no_terminal

Don't enable the interactive terminal

Action: store_false

---

### no_clean_slate

Don't make a new tab when starting with an input

Action: store_false

---

### no_more_button

Don't show the More button

Action: store_false

---

### no_model_icon

Don't show the model icon

Action: store_false

---

### no_model_feedback

Don't show model feedback when loading

Action: store_false

---

### no_log_feedback

Don't show feedback when saving logs

Action: store_false

---

### no_emojis

Don't use emojis

Action: store_false

---

### no_input_memory

Don't remember input words

Action: store_false

---

### no_write_button

Don't show the textbox button

Action: store_false

---

### no_wrap_textbox

Don't wrap the textbox text

Action: store_false

---

### no_markdown_snippets

Don't do snippet markdown

Action: store_false

---

### no_markdown_italic

Don't do italic markdown

Action: store_false

---

### no_markdown_bold

Don't do bold markdown

Action: store_false

---

### no_markdown_highlights

Don't do highlight markdown

Action: store_false

---

### no_markdown_urls

Don't do URL markdown

Action: store_false

---

### no_log_errors

Don't log error messages to a file

Action: store_false

---

### no_time

Don't show the loading time at startup

Action: store_false

---

### no_gestures

Don't enable mouse gestures

Action: store_false

---

### no_increment_logs

Always use the file name, don't increment with numbers

Action: store_false

---

### no_confirm_urls

No need to confirm when opening URLs

Action: store_false

---

### no_confirm_search

No need to confirm when searching

Action: store_false

---

### no_confirm_close

No need to confirm closing tabs

Action: store_false

---

### no_confirm_clear

No need to confirm clearing conversations

Action: store_false

---

### no_fill_prompt

Don't fill the text input prompt in some cases when empty

Action: store_false

---

### no_drag_and_drop

Don't enable drag and drop

Action: store_false

---

### no_keywords

Don't do keyword replacements like ((now))

Action: store_false

---

### no_prevnext

Don't show the Prev and Next buttons

Action: store_false

---

### no_auto_name

Don't auto-name tabs based on input

Action: store_false

---

### no_tab_double_click

Open new tabs on double click

Action: store_false

---

### no_labels

Don't show the labels

Action: store_false

---

### no_syntax_highlighting

Don't apply syntax highlighting to snippets

Action: store_false

---

### test

Make a test tab for debugging

Default: False

Action: store_true

---

### force

Allow opening multiple instances

Default: True

Action: store_true

---

### confirm_exit

Show confirm exit dialog

Default: False

Action: store_true

---

### compact_model

Hide the model frame in compact mode

Default: False

Action: store_true

---

### compact_system

Hide the system frame in compactm ode

Default: False

Action: store_true

---

### compact_details_1

Hide the first details frame in compact mode

Default: False

Action: store_true

---

### compact_details_2

Hide the second details frame in compact mode

Default: False

Action: store_true

---

### compact_buttons

Hide the buttons frame in compact mode

Default: False

Action: store_true

---

### compact_file

Hide the URL frame in compact mode

Default: False

Action: store_true

---

### compact_input

Hide the input frame in compact mode

Default: False

Action: store_true

---

### maximize

Maximize the window on start

Default: False

Action: store_true

---

### numbers

Show numbers in the tab bar

Default: False

Action: store_true

---

### alt_palette

Show commands instead of descriptions in the palette

Default: False

Action: store_true

---

### terminal_vi

Use vi mode in the terminal

Default: False

Action: store_true

---

### tabs_always

Always show the tab bar even if only one tab

Default: False

Action: store_true

---

### verbose

Make the model verbose when streaming

Default: False

Action: store_true

---

### quiet

Don't show some messages

Default: False

Action: store_true

---

### debug

Show some information for debugging

Default: False

Action: store_true

---

### display

Only show the output and tabs

Default: False

Action: store_true

---

### listener

Listen for changes to the stdin file

Default: False

Action: store_true

---

### sticky

Make the window always on top

Default: False

Action: store_true

---

### avatars_in_logs

Show avatars in text logs

Default: False

Action: store_true

---

### short_labels

Use the short version of labels

Default: False

Action: store_true

---

### short_buttons

Use the short version of buttons

Default: False

Action: store_true

---

### errors

Show error messages

Default: False

Action: store_true

---

### terminal_height

Reserve these number of rows for the terminal

Default: 3

Type: int

---

### width

Width of the window

Default: -1

Type: int

---

### height

Height of the window

Default: -1

Type: int

---

### max_tabs

Max number fo tabs to keep open

Default: 0

Type: int

---

### max_tab_width

Max number of characters to show in a tab name

Default: 0

Type: int

---

### config

Name or path of a config file to use

Default: ""

Type: str

---

### session

Name or path of a session file to use

Default: ""

Type: str

---

### on_log

Command to execute when saving any log file

Default: ""

Type: str

---

### on_log_text

Command to execute when saving a text log file

Default: ""

Type: str

---

### on_log_json

Command to execute when saving a JSON log file

Default: ""

Type: str

---

### f1

Command to assign to the F1 key

Default: "/help"

Type: str

---

### f2

Command to assign to the F2 key

Default: ""

Type: str

---

### f3

Command to assign to the F3 key

Default: "/next"

Type: str

---

### f4

Command to assign to the F4 key

Default: ""

Type: str

---

### f5

Command to assign to the F5 key

Default: "/reset"

Type: str

---

### f6

Command to assign to the F6 key

Default: ""

Type: str

---

### f7

Command to assign to the F7 key

Default: ""

Type: str

---

### f8

Command to assign to the F8 key

Default: "/compact"

Type: str

---

### f9

Command to assign to the F9 key

Default: ""

Type: str

---

### f10

Command to assign to the F10 key

Default: ""

Type: str

---

### f11

Command to assign to the F11 key

Default: "/fullscreen"

Type: str

---

### f12

Command to assign to the F12 key

Default: "/list"

Type: str

---

### input

Prompt the AI automatically with this input when starting the program

Default: ""

Type: str

---

### alias

Define an alias to run commands

Action: append

Type: str

---

### task

Define a task to run periodically

Action: append

Type: str

---

### gesture_threshold

Threshold in pixels for mouse gestures

Default: 33

Type: str

---

### scroll_lines

How many lines to scroll the output

Default: 1

Type: int

---

### auto_name_length

Max char length for auto tab names

Default: 35

Type: int

---

### old_tabs_minutes

Consider a tab old after these minutes (using last modified date)

Default: 30

Type: int

---

### max_list_items

Max number of items in context menu lists

Default: 10

Type: int

---

### list_item_width

Max characters for the text of list items

Default: 100

Type: int

---

### drag_threshold

The higher the number the less sensitive the tab dragging will be

Default: 88

Type: int

---

### delay

Delay in seconds between each print when streaming

Default: 0.1

Type: float

---

### prefix

Character used to prefix commands like /

Default: "/"

Type: str

---

### andchar

Character used to join commands like &

Default: "&"

Type: str

---

### system_threshold

Show system monitors as critical after this percentage threshold

Default: 70

Type: int

---

### system_delay

Delay in seconds for system monitor updates

Default: 3

Type: int

---

### autorun

Run this command at startup

Default: ""

Type: str

---

### input_memory_min

Minimum number of characters for input words to be remembered

Default: 4

Type: int

---

### listener_delay

Delay for the listener checks

Default: 0.5

Type: float

---

### commandoc

Make the commandoc and save it on this path

Default: "commands.md"

Type: str

---

### argumentdoc

Make the argument and save it on this path

Default: "arguments.md"

Type: str

---

### after_stream

Execute this command after streaming a response

Default: ""

Type: str

---

### markdown

Define where to apply markdown formatting

Default: "ai"

Choices: user, ai, all, none

Type: str

---

### browser

Open links with this browser

Default: ""

Type: str

---

### font_diff

Add or subtract this from font sizes

Default: 0

Type: int

---

### task_manager

Which task manager to use

Default: "auto"

Type: str

---

### task_manager_gpu

Which task manager to use on the gpu monitors

Default: "auto"

Type: str

---

### terminal

Which terminal to use

Default: "auto"

Type: str

---

### progtext

Use this program as default for the progtext command

Default: ""

Type: str

---

### progjson

Use this program as default for the progjson command

Default: ""

Type: str

---

### program

Use this program as default for the progtext and progjson commands

Default: ""

Type: str

---

### user_color

The color of the text for the name of the user

Default: "auto"

Type: str

---

### ai_color

The color of the text for the name of the AI

Default: "auto"

Type: str

---

### snippets_font

The font to use in snippets

Default: "monospace"

Type: str

---

### emoji_unloaded

Emoji to show when a model is not loaded

Default: "👻"

Type: str

---

### emoji_local

Emoji to show when a model is loaded locally

Default: "✅"

Type: str

---

### emoji_remote

Emoji to show when a model is loaded remotely

Default: "🌐"

Type: str

---

### emoji_loading

Emoji to show when loading a model

Default: "⏰"

Type: str

---

### emoji_storage

Emoji to show when saving a log

Default: "💾"

Type: str

---

### name_mode

What mode to use when naming new tabs

Default: "random"

Choices: random, noun, empty

Type: str