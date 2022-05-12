# nagcat

A helpful cat which nags you from the tmux statusbar... because she loves you! *(Cat pronoun can be customized.)*

The kitty doesn't actively notify you at a specific time. If a reminder is set for 2pm, she might not notice for a while. But eventually she'll put a little reminder in the statusbar! Until then, you can always `nagcat pet` her for comfort or to snooze a reminder. For a reminder of what your reminder is, say `nagcat why` to the kitty 🐈

Written with pure Python 3.8+ for Linux, though I would like to support macOS and Windows too! Please submit an issue or pull request if you have any problems or suggestions for improvement.

The nagcat tmux plugin is written for Bash 4, although it should work with Bash 3 as well.


## Quick overview

* By default, nagcat will return `=^.^=` if you have no reminders pending
* nagcat will return [!!!] if you should drink water (once per day at 2pm)
* Reminders are stored in a simple JSON file editable with `nagcat config`
* Try `nagcat -h` for a full list of "commands" (nagcat likes to think of them as "suggestions")


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
