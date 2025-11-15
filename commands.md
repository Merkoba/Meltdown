# Commands

Commands can be chained:

```
/tab 2 & /sleep 0.5 & /select
```

This will select tab 2, then wait 500ms, then select all.

Here are all the available commands:

---

### clear

Clear the conversation

Use 'force' to force

---

### exit

Exit the application

Optional delay in seconds

---

### like

Send a like prompt

---

### dislike

Send a dislike prompt

---

### cancelexit

Cancel the exit if you had set a delay

---

### compact

Toggle compact mode

---

### log

Show the log menu

---

### logtext

Save conversation to a text file

---

### logjson

Save conversation to a JSON file

---

### logmarkdown

Save conversation to a markdown file

---

### logtextall

Save all conversations to text files

---

### logjsonall

Save all conversations to JSON files

---

### logmarkdownall

Save all conversations to markdown files

---

### resize

Resize the window. You can provide dimensions like 800x600

---

### stop

Stop the current stream

---

### taskmanager

Open the system task manager

---

### top

Scroll to the top

---

### bottom

Scroll to the bottom

---

### maximize

Maximize the window

---

### close

Close current tab

Use 'force' to force

---

### closeothers

Close other tabs

Use 'force' to force

---

### closeall

Close all tabs

Use 'force' to force

---

### closeold

Close old tabs

Use 'force' to force

---

### closeoldest

Close oldest tab

Use 'force' to force

---

### closeempty

Close empty tabs

Use 'force' to force

---

### closepins

Close all pinned tabs

Use 'force' to force

---

### closenormal

Close all normal tabs

Use 'force' to force

---

### closeleft

Close tabs to the left

Use 'force' to force

---

### closeright

Close tabs to the right

Use 'force' to force

---

### closepicked

Close picked tabs

Use 'force' to force

---

### closehalf

Close the first half of the tabs

Use 'force' to force

---

### refresh

Refresh the conversation

---

### replay

Replay the conversation, one message at a time, mainly to debug

---

### new

Make a new tab. Optional argument for the name

---

### newstart

Make a new tab at the start. Optional argument for the name

---

### about

Show the about window

---

### help

Show the help overview

You can filter by text

---

### commands

Show the commands help

You can filter by text

---

### arguments

Show the arguments help

You can filter by text

---

### keyboard

Show the keyboard help

You can filter by text

---

### list

Show the tab list to pick a tab

---

### find

Find a text string

---

### findall

Find a text string among all tabs

---

### findallprev

Find a text string among all tabs (backwards)

---

### first

Go to the first tab

---

### last

Go to the last tab

---

### middle

Go to the middle of tabs

---

### config

Config menu or view, set, reset a config

---

### session

Show the session menu

---

### reset

Reset all configs

---

### copytext

Copy raw text

---

### copyjson

Copy raw JSON

---

### copymarkdown

Copy raw Markdown

---

### viewtext

View raw text

---

### viewjson

View raw JSON

---

### viewmarkdown

View raw Markdown

---

### move

Move tab to the start or end

---

### tab

Go to a tab by its number or by its name

---

### fullscreen

Toggle fullscreen

---

### findprev

Find previous text match

---

### findnext

Find next text match

---

### scrollup

Scroll up

---

### scrollupmore

Scroll up more

---

### scrolldown

Scroll down

---

### scrolldownmore

Scroll down more

---

### load

Load the model

---

### unload

Unload the model

---

### context

Show the context list

---

### left

Go to the tab on the left

---

### right

Go to the tab on the right

---

### moveleft

Move the tab to the left

---

### moveright

Move the tab to the right

---

### movestart

Move the tab to the start

---

### moveend

Move the tab to the end

---

### main

Show the main menu

---

### savesession

Save the current session

You can provide a file name. You can use 'last'

---

### loadsession

Load a session

You can provide a file name. You can use 'last'

---

### saveconfig

Save the current config

You can provide a file name. You can use 'last'

---

### loadconfig

Load a config

You can provide a file name. You can use 'last'

---

### copyall

Copy all the text

---

### selectall

Select all text

---

### deselect

Deselect all text

---

### model

Show the model menu

---

### recent

Show the recent models

---

### browse

Browse the models

---

### file

Browse for a file

---

### palette

Show the command palette

---

### rename

Rename the tab

---

### prompt

Make a new tab and use this prompt

---

### promptforce

Force a new tab and use this prompt

---

### write

Write an input prompt

---

### writemax

Write an input prompt and maximize

---

### type

Set the input to this text

---

### sleep

Wait x seconds before the next command

---

### hide

Close dialogs and menus

---

### printconfig

Print all the config settings

---

### bigger

Increase the font size

---

### smaller

Decrease the font size

---

### font

Set the font size

---

### fontfamily

Set the font family

---

### resetfont

Reset the font

---

### togglescroll

Scroll to the bottom or to the top

---

### stats

Show some internal information

---

### memory

Show how much memory the program is using

---

### started

How long ago the program started

---

### sticky

Make the window stay at the top

---

### commandoc

Make a file with all the commands

---

### argumentdoc

Make a file with all the arguments

---

### keyboardoc

Make a file with all the keyboard shortcuts

---

### active

Go to the tab that is currently streaming

---

### system

Write the system prompt

---

### more

Show the more menu

---

### tabmenu

Show the tab menu

---

### fontmenu

Show the font menu

---

### openai

Show the OpenAI menu

---

### google

Show the Google menu

---

### anthropic

Show the Anthropic menu

---

### openaikey

Set the OpenAI API key

---

### googlekey

Set the Google API key

---

### anthropickey

Set the Anthropic API key

---

### opentext

Open a program using the text

---

### openjson

Open a program using the JSON

---

### openmarkdown

Open a program using the markdown

---

### usetext

Use the current text (text)

---

### usejson

Use the current text (JSON)

---

### usemarkdown

Use the current text (markdown)

---

### submit

Submit the input

---

### fresh

Do a prompt without using the history

---

### change

Set a model by its name

---

### mode

Change the model mode

---

### toggletabs

Toggle tabs visibility

---

### summarize

Summarize the conversation

---

### delete

Remove a specific item of a conversation

You can use a specific number, or words like 'first' and 'last'

---

### deleteabove

Delete items above this item

You can use a specific number, or words like 'first' and 'last'

---

### deletebelow

Delete items below this item

You can use a specific number, or words like 'first' and 'last'

---

### deleteothers

Delete the other items

You can use a specific number, or words like 'first' and 'last'

---

### openfile

Open the last file used

---

### date

Show the current date and time

---

### explain

Explain selected words

---

### newexplain

Open a new tab and explain something

---

### search

Search using the selected text

---

### copymenu

Copy the last item

---

### copy

Copy the last user and AI text

---

### copyuser

Copy the last user text

---

### copyai

Copy the last AI text

---

### args

Show the arguments used

---

### prev

Go to the previous tab

---

### nothing

Do nothing

---

### random

Make up a random prompt

---

### toggleframe

Toggle a specific frame

---

### showframe

Show a specific frame

---

### hideframe

Hide a specific frame

---

### lastlog

Open the last log

---

### autoscroll

Toggle automatic scrolling

Optional up or down argument

---

### autoscrollup

Toggle automatic scrolling (Up)

---

### startautoscroll

Start automatic scrolling

Optional up or down argument

---

### autoscrollstop

Stop automatic scrolling

---

### faster

Make auto-scroll faster

---

### slower

Make auto-scroll slower

---

### repeat

Repeat the specified prompt (considering history up to that point)

---

### repeatclean

Repeat the specified prompt (without history)

---

### repeatfull

Repeat the specified prompt (with all the history)

---

### copyitem

Copy the specified item

---

### selectitem

Select the specified item

---

### use

Use the specified item

---

### info

Show information about the specified item

---

### profile

Show the current profile

---

### portrait

Show the AI's portrait

---

### describe

The describe prompt

---

### theme

Show the theme menu

---

### modelname

Show the model name

---

### size

Show size and length information

---

### information

Show the info dialog

---

### upload

Start an upload. Optional 'all' or 'last' argument

---

### uploadfull

Start a full upload process. Optional 'all' or 'last' argument

---

### uploadharambe

Start a Harambe upload. Optional 'all' or 'last' argument

---

### uploadrentry

Start a Rentry upload. Optional 'all' or 'last' argument

---

### uploadmarkdown

Upload markdown to a hosting service. Optional 'all' or 'last' argument

---

### uploadraw

Upload raw to a hosting service. Optional 'all' or 'last' argument

---

### uploadjson

Upload json to a hosting service. Optional 'all' or 'last' argument

---

### uploadtext

Upload text to a hosting service. Optional 'all' or 'last' argument

---

### count

Count the number of open tabs and items

---

### signal

Run a signal by its name

---

### arg

Set an argument while the program is running

---

### setvar

Set a variable. For example: /setvar x the world. Then use it with $x

---

### unsetvar

Unset a variable

---

### readvar

Read the content of a variable

---

### vars

Read all the variables

---

### print

Print a message

---

### echo

Print a message and format markdown

---

### pin

Pin a tab

---

### unpin

Unpin a tab

---

### togglepin

Pin or unpin a tab

---

### pins

Show the tab list but only with pins

---

### sortpins

Place the pins at the start of the list

---

### sortpinsend

Place the pins at the end of the list

---

### image

Generate an image through a prompt

---

### setalias

Set an alias. For example: /setalias pro /loadconfig pro

---

### unsetalias

Unset an alias

---

### readalias

Read the content of an alias

---

### say

Say something exactly as it is

---

### program

Use a program with the last AI response

---

### notify

Show a notification message using notify-send

---

### filter

Filter the conversation by a specific text

---

### randomconfig

Randomize some config settings

---

### script

Use a registered script using the current conversation

---

### enabletasks

Enable automatic tasks

---

### disabletasks

Disable automatic tasks

---

### snippets

Print the number of snippets

---

### locket

Ask about a locket
