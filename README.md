# nagcat

A helpful cat which nags you from the tmux statusbar... because she loves you!

nagcat doesn't actively notify you like an alarm clock. It's a simple command that returns `=^.^=` if you have no reminders, or `=u.u=` if you have overdue reminders.

Use `nagcat pet` to dismiss all current reminders for this day.

For a reminder of what the latest reminder is, say `nagcat why` 🐈

You may use the included `nagcat.tmux` plugin for tmux, or simply use nagcat on its own!


---


## Installation with Pip

1. Install using Pip:
    * `pip install nagcat`

1. Add to tmux statusbar by editing `.tmux.conf`:
    * `set -g status-right '#{nagcat}'`
    * `run-shell nagcat.tmux`


### Updating with Pip
* `pip install --upgrade nagcat`


---


## Installation with [Tmux Plugin Manager](https://github.com/tmux-plugins/tpm)

1. Add to list of TPM plugins:
    * `set -g @plugin 'tassaron/nagcat'`

1. Hit `prefix` + <kbd>I</kbd> to download the plugin

1. Add to tmux statusbar by editing `.tmux.conf`:
    * `set -g status-right '#{nagcat}'`


###  Updating with Tmux Plugin Manager

* Use TPM update command: `prefix` + <kbd>U</kbd>


---


## Which Installation Method to Use?

On most operating systems, installing with Pip will automatically put the `nagcat` command in the $PATH. Other than convenience and personal preference, there is no difference between the installation methods. You can safely install using both methods on the same system if you change your mind in the future.

### Make an alias to TPM-installed version
* Add to bottom of `.bashrc`:
```
alias nagcat="python $HOME/.tmux/plugins/nagcat/src nagcat.py"
```
* Replace `python` with `python3` on some Linux distros (Debian, Ubuntu)


---


## Editing Reminders:

### ~/.config/nagcat/reminders.json

```
{
    "09:00": "Time for breakfast",
    "14:00": "You should drink water"
}
```

* Safely edit this JSON file with `nagcat config`
* If `$EDITOR` is not set in your shell, set nagcat's preferred text editor using `nagcat config -e path/to/editor`
* If you edit `reminders.json` manually and make a mistake, nagcat might stop working. Delete the invalid file to fix this.
* nagcat only supports daily reminders and 24-hour time
* The default reminder is "Drink water" at 14:00
* JSON looks like a Python dictionary, but does **not** allow extra commas.


---


## Customization

### Tmux Hotkeys

* `prefix` + <kbd>W</kbd>: Runs `nagcat why` and shows output
* `prefix` + <kbd>P</kbd>: Runs `nagcat pet` to dismiss current reminders
* Change hotkeys from default <kbd>W</kbd> & <kbd>P</kbd> to _e.g.,_ <kbd>e</kbd> & <kbd>r</kbd>:
```
set -g @nagcat_why e
set -g @nagcat_pet r
```


### Appearance

* Make it _your_ nagcat &mdash; see `nagcat config -h` for details
* Change appearance (face/alert), name, pronoun
* *E.g.,* how to remove cat theming: `nagcat config -face '' -alert '!!!'`


### Use in a Graphical Environment

You may also use nagcat in a graphical environment using something like *e.g.* [the Command Output widget for KDE Plasma](https://store.kde.org/p/1166510). To output your reminder text into a graphical pop-up window, try one of these commands:
* `zenity --info --text="$(nagcat why)" --no-markup --no-wrap`
* `kdialog --msgbox "$(nagcat why)"`


---


## Reporting bugs

Please include some details when reporting bugs, such as:
* Your OS
* `nagcat --version`
* `bash --version`
* `python --version` (or `python3`)
* `tmux -V`
* If you're using TPM, pip, a venv, some combination of these, etc.
