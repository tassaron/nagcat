# nagcat

A helpful cat which nags you from the tmux statusbar... because she loves you! *(Cat name and pronoun can be customized.)*

nagcat doesn't actively notify you at a specific time. If a reminder is set for 9 in the morning, she might not notice for a while; so it's not an alarm clock! nagcat will put a little `=u.u=` in the statusbar sometime after your reminder is set to trigger, as a friendly nag! :)

Use `nagcat pet` to dismiss the reminder. For a reminder of what the reminder is, say `nagcat why` 🐈

Written with pure Python 3.8+ for Linux or WSL, although it probably works anywhere with modern versions of Python, Bash, and tmux. Please submit an issue or pull request if you have any problems or suggestions for improvement.


## Quick overview

* By default, nagcat will return `=^.^=` if you have no reminders pending
* By default, nagcat will return `=u.u=` if you should drink water, after 14:00, until you `nagcat pet` her
* Reminders are stored in a simple JSON file editable with `nagcat config`
* Try `nagcat -h` for a full list of "commands" (nagcat likes to think of them as "suggestions")
* Easily customize nagcat's name, pronoun, and appearance -- see `nagcat config -h`
* To remove cat theming: `nagcat config -face '' -alert [\!]`


## Installation

1. `pip install nagcat` to get the latest stable version from PyPI

1. Use nagcat manually by running `nagcat` from a terminal

1. To put nagcat output in tmux statusbar:
    * Add `run-shell nagcat.tmux` to the bottom of `.tmux.conf`
    * Add `#{nagcat}` to your tmux `status-right` or `status-left`


## Example setup

### ~/.config/nagcat/reminders.json **(safely edit with `nagcat config`)**
```
{
    "09:00": "Time for breakfast",
    "14:00": "You should drink water",
}
```

nagcat currently only supports 24-hour time and daily reminders.

### ~/.tmux.conf **(`nagcat` and `nagcat.tmux` must be on $PATH)**
```
set -g status-right '#{nagcat}'
run-shell nagcat.tmux
```


## Updating

1. `pip install --upgrade nagcat` should be sufficient!

1. If something goes wrong, try a "factory reset": `nagcat config --reset`
