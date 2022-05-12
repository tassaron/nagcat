# nagcat

A helpful cat which nags you from the tmux statusbar... because she loves you! *(Cat name and pronoun can be customized.)*

nagcat doesn't actively notify you at a specific time. If a reminder is set for 9 in the morning, she might not notice for a while; so it's not an alarm clock! nagcat will put a little `[!!!]` in the statusbar sometime after your reminder is set to trigger, as a friendly nag! :)

Use `nagcat pet` to dismiss the reminder. For a reminder of what the reminder is, say `nagcat why` 🐈

Written with pure Python 3.8+ for Linux or WSL, although it probably works anywhere with modern versions of Python, Bash, and tmux. Please submit an issue or pull request if you have any problems or suggestions for improvement.


## Quick overview

* By default, nagcat will return `=^.^=` if you have no reminders pending
* By default, nagcat will return `=u.u=` if you should drink water, after 14:00, until you `nagcat pet` her
* Reminders are stored in a simple JSON file editable with `nagcat config`
* Try `nagcat -h` for a full list of "commands" (nagcat likes to think of them as "suggestions")
* Easily customize nagcat's name, pronoun, and appearance - see `nagcat config -h` for details
    * If you want to change `=u.u=` to something like `!!!` using the CLI, do `nagcat config -alert \!\!\!`

## Example of reminders.json
```
{
    "09:00": "morning jog",
    "14:00": "drink water",
}
```

nagcat currently only supports 24-hour time and daily reminders.


## Installation

1. `pip install nagcat` to get the latest stable version from PyPI

1. Use nagcat manually by running `nagcat` from a terminal

1. To put nagcat output in tmux statusbar:
    * Add `run-shell nagcat.tmux` to the bottom of `.tmux.conf`
    * Add `#{nagcat}` to your tmux `status-right` or `status-left`


## Updating

1. `pip install --upgrade nagcat` should be sufficient!

1. If new keys are added to the config file in an update, nagcat will write default values into the config when it needs them.


## Development

* Free the three! `sudo apt install python-is-python3` =^.^=
* Use black formatter: `pip install black` and use `black` command
* Run tests: `pip install pytest` and use `pytest` command
* Handle cross-module concerns in `__main__.py` so the imports don't get out of hand
    * The only inter-package import should be the `logger` from `__init__.py`
* In this house, we use typehints for some reason 🤷‍♀️
