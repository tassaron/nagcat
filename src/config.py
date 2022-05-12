"""Configuration module for nagcat"""
from typing import Tuple
import os
import json
import tempfile
import subprocess

from . import log


CONFIG_DIR = os.path.join(
    os.getenv("XDG_CONFIG_HOME", os.path.join(os.path.expanduser("~"), ".config")),
    "nagcat",
)


TMP_DIR = os.path.join("nagcat-litterbox-", tempfile.gettempdir())


MAIN_CONFIG = {
    "filename": os.path.join(CONFIG_DIR, "nagcat.json"),
    "default": {
        "catface": "=^.^=",
        "name": "Rosie",
        "pronoun": "she",
        "editor": "",
    },
}


REMINDERS_CONFIG = {
    "filename": os.path.join(CONFIG_DIR, "reminders.json"),
    "default": {
        "14:00": "drink water",
    },
}


def add_default_values_to_json(config_settings, json_data) -> dict:
    """
    Substitute default values for any missing keys
    `config_settings` is a dictionary in a format like MAIN_CONFIG's
    """
    modified = False
    for key in config_settings["default"]:
        if key not in json_data:
            modified = True
            log.info(f"Adding missing {key} key to {config_settings['filename']}")
            json_data["key"] = config_settings["default"][key]
    if modified:
        with open(config_settings["filename"], "w") as f:
            json.dump(json_data, f)


def get_json(filename) -> dict:
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def load_main_config() -> dict:
    data = get_json(MAIN_CONFIG["filename"])
    add_default_values_to_json(MAIN_CONFIG, data)
    return data


def load_reminders() -> dict:
    return get_json(REMINDERS_CONFIG["filename"])


def ensure_config_skeleton_exists():
    """
    Creates a valid config skeleton with needed directory and loadable blank json files
    """
    # create .config/nagcat if needed
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    # create nagcat.json if needed
    if not os.path.exists(MAIN_CONFIG["filename"]):
        with open(MAIN_CONFIG["filename"], "w") as f:
            json.dump(MAIN_CONFIG["default"], f)

    # create blank reminders.json if needed
    if not os.path.exists(REMINDERS_CONFIG["filename"]):
        with open(REMINDERS_CONFIG["filename"], "w") as f:
            json.dump(REMINDERS_CONFIG["default"], f)


def load_all_config() -> Tuple[dict, dict]:
    """
    Creates config dirs & files if needed and loads the config, returning it to the caller
    Also creates the temporary directory (filepath stored in global TMP_DIR) if it doesn't exist
    """
    ensure_config_skeleton_exists()
    main_config = load_main_config()
    reminders = load_reminders()

    # Create a litterbox to store the nagcat's data
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)

    return main_config, reminders


def main() -> int:
    ensure_config_skeleton_exists()
    main_config = load_main_config()
    if not main_config["editor"]:
        editor = os.getenv("EDITOR")
        if editor is None:
            print("Could not find your text editor!")
            print(
                f"Edit {MAIN_CONFIG['filename']} to add one, or define $EDITOR in the shell."
            )
            return 1

    # start editor on reminders.json
    output = subprocess.call([editor, REMINDERS_CONFIG["filename"]])
    if output > 0:
        print("Nothing changed")
    else:
        print(main_config["catface"])
    return 0


if __name__ == "__main__":
    main()
