# nagcat

A helpful cat which nags you from the tmux statusbar... because she loves you!

nagcat doesn't actively notify you like an alarm clock. It's a simple command that returns `=^.^=` if you have no reminders, or `=u.u=` if you have overdue reminders.

Use `nagcat pet` to dismiss all current reminders for this day.

For a reminder of what the latest reminder is, say `nagcat why` 🐈

You may use the included `nagcat.tmux` plugin for tmux, or simply use nagcat on its own!


## Installation

1. `pip install nagcat`

1. To put nagcat output in tmux statusbar:
    * Add `run-shell nagcat.tmux` to the bottom of `.tmux.conf`
    * Add `#{nagcat}` to your tmux `status-right` or `status-left`


### Updating

1. `pip install --upgrade nagcat`

1. If something goes wrong, try a "factory reset" with `nagcat config --reset`


## Example setup

---

### ~/.config/nagcat/reminders.json **(safely edit with `nagcat config`)**
```
{
    "09:00": "Time for breakfast",
    "14:00": "You should drink water"
}
```

_Note:_ nagcat currently only supports 24-hour time and daily reminders.

---

### ~/.tmux.conf **(`nagcat` and `nagcat.tmux` must be on $PATH)**

```
set -g status-right '#{nagcat}'
run-shell nagcat.tmux
```

---


## Customization

* The default reminder is "Drink water" at 14:00
* Reminders are stored in a JSON file which is safely editable with `nagcat config`
* Try `nagcat -h` for a full list of "suggestions" you can make (cats don't accept "commands")
* Easily customize nagcat to make it _your_ nagcat ;) &mdash; see `nagcat config -h` for details
* Customization includes appearance, name, pronoun, and preferred text editor
* *E.g.,* how to remove cat theming: `nagcat config -face '' -alert '!!!'`

### Use in a Graphical Environment

You may also use nagcat in a graphical environment using something like *e.g.* [the Command Output widget for KDE Plasma](https://store.kde.org/p/1166510). To output your reminder text into a graphical pop-up window, try one of these commands:
* `zenity --info --text="$(nagcat why)" --no-markup --no-wrap`
* `kdialog --msgbox "$(nagcat why)"`
