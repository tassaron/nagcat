"""Configuration module for nagcat"""
from typing import Tuple
import os
import json
import tempfile


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
    },
}


REMINDERS_CONFIG = {
    "filename": os.path.join(CONFIG_DIR, "reminders.json"),
    "default": {
        "14:00": "drink water",
    },
}


def get_json(filename) -> dict:
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def get_config() -> dict:
    return get_json(MAIN_CONFIG["filename"])


def get_reminders() -> dict:
    return get_json(REMINDERS_CONFIG["filename"])


def load_config() -> Tuple[dict, dict]:
    """
    Creates config dirs & files if needed and loads the config, returning it to the caller
    Also creates the temporary directory (filepath stored in global TMP_DIR) if it doesn't exist
    """

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

    ensure_config_skeleton_exists()
    main_config = get_config()
    reminders = get_reminders()

    # Create a litterbox to store the nagcat's data
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)

    return main_config, reminders


def main():
    main_config, reminders = load_config()
    print(main_config["catface"])
    print(reminders)


if __name__ == "__main__":
    main()
