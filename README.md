# nagcat

A helpful cat which nags you from within the tmux statusbar... because she loves you!

The kitty doesn't actively notify you at a specific time. If a reminder is set for 2pm, she might not notice for a while. But eventually she'll put a little reminder in the statusbar! Until then, you can always `nagcat pet` her for comfort or to snooze a reminder. For a reminder of what your reminder is, say `nagcat what` to the kitty 🐈


## Quick overview
* Install (see instructions below), then add `#{nagcat}` to your tmux `status-right` or `status-left`
* By default, nagcat will put a `=^.^=` if you have no reminders pending, or a [!!!] if you should drink water (once per day at 2pm).
* Customizable with simple JSON files. Currently supports multiple daily reminders at customizable time.
* Customizable cat face, name, and pronouns!


## Installation
1. `pip install nagcat` to get the latest stable version from PyPI
1. Open editor for `cron`, which is a task scheduler:
    crontab -e
1. Add a crontab entry for nagcat at the bottom of the file:
    */20 * * * * /usr/bin/env python3 -m nagcat
1. Refresh nagcat manually with `nagcat` command or `python3 -m nagcat`

## Note
`sudo apt install python-is-python3` =^.^= < free the three!)
