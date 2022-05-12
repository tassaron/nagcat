"""Configuration module for nagcat"""
from typing import List, Tuple, Dict
import os
import json
import argparse
import subprocess

from . import logger


CONFIG_DIR = os.path.join(
    os.getenv("XDG_CONFIG_HOME", os.path.join(os.path.expanduser("~"), ".config")),
    "nagcat",
)


MAIN_CONFIG_FILE = os.path.join(CONFIG_DIR, "nagcat.json")


REMINDERS_CONFIG_FILE = os.path.join(CONFIG_DIR, "reminders.json")


MAIN_CONFIG_DEFAULT: Dict[str, str] = {
    "catface": "=^.^=",
    "name": "Rosie",
    "pronoun": "she",
    "editor": os.getenv("EDITOR", "/usr/bin/nano"),
}


REMINDERS_CONFIG_DEFAULT: Dict[str, str] = {
    "14:00": "drink water",
}


def save_json(filename: str, json_data: Dict[str, str]):
    """Overwrite destination file with json data"""
    with open(filename, "w") as f:
        json.dump(json_data, f)


def add_default_values_to_json(
    config_file: str, default_config: Dict[str, str], json_data: Dict[str, str]
) -> None:
    """Substitute default values for any missing keys"""
    modified = False
    for key in default_config:
        if key not in json_data:
            modified = True
            logger.info(f"Adding missing {key} key to {config_file}")
            json_data["key"] = default_config[key]
    if modified:
        save_json(config_file, json_data)


def get_json(filename: str) -> Dict[str, str]:
    """Receives path to json file, returns the data as a dict[str, str]"""
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def load_main_config() -> Dict[str, str]:
    """Load nagcat.json as a dict[str, str]"""
    data = get_json(MAIN_CONFIG_FILE)
    add_default_values_to_json(MAIN_CONFIG_FILE, MAIN_CONFIG_DEFAULT, data)
    return data


def load_reminders() -> Dict[str, str]:
    """Load reminders.json as a dict[str, str]"""
    return get_json(REMINDERS_CONFIG_FILE)


def ensure_config_skeleton_exists() -> None:
    """If needed, creates a config skeleton with needed directory and loadable blank json files"""
    # create .config/nagcat if needed
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    # create nagcat.json if needed
    if not os.path.exists(MAIN_CONFIG_FILE):
        save_json(MAIN_CONFIG_FILE, MAIN_CONFIG_DEFAULT)

    # create blank reminders.json if needed
    if not os.path.exists(REMINDERS_CONFIG_FILE):
        save_json(REMINDERS_CONFIG_FILE, REMINDERS_CONFIG_DEFAULT)


def load_all_config() -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Creates config dirs & files if needed and loads the config, returning it to the caller
    Also creates the temporary directory (filepath stored in global TMP_DIR) if it doesn't exist
    """
    ensure_config_skeleton_exists()
    main_config = load_main_config()
    reminders = load_reminders()

    return main_config, reminders


def create_argparser(main_config: Dict[str, str]) -> argparse.ArgumentParser:
    """Create and return an argparser for this commandline entrypoint"""
    parser = argparse.ArgumentParser(
        description=f"Tell {main_config['name']} how {main_config['pronoun']} can help you better",
        epilog=main_config["catface"],
    )
    parser.add_argument(
        "-name",
        help=f"give {main_config['name']} a new name",
        nargs=1,
    )
    parser.add_argument(
        "-pronoun",
        help=f"change '{main_config['pronoun']}' to a different pronoun",
        nargs=1,
    )
    parser.add_argument(
        "-face",
        help=f"change {main_config['catface']} to something else",
        nargs=1,
    )
    parser.add_argument(
        "-editor",
        help=f"set text editor for editing reminders.json",
        nargs=1,
    )
    parser.add_argument(
        "--reset",
        help="delete all nagcat files!",
        action="store_true",
    )

    return parser


def main(argv: List) -> int:
    """Commandline entrypoint"""
    ensure_config_skeleton_exists()
    main_config = load_main_config()

    editor = main_config["editor"]
    if not editor:
        editor = os.getenv("EDITOR")
        if not editor:
            print("Could not find your text editor!")
            print("Set the text editor with `nagcat config -e /path/to/editor`")
            print("or set the $EDITOR environment variable in your shell.")
            return 1

    if not argv:
        # start editor on reminders.json
        output = subprocess.call([editor, REMINDERS_CONFIG_FILE])
        if output > 0:
            print("Nothing changed")
        else:
            print(main_config["catface"])
        return 0

    parser = create_argparser(main_config)
    args = parser.parse_args(argv)

    # At this point argparse has returned 1 or higher if args are bad
    # So we always return 0 because one of these conditions should be true

    if args.reset:
        os.remove(MAIN_CONFIG_FILE)
        os.remove(REMINDERS_CONFIG_FILE)
        os.rmdir(CONFIG_DIR)
        ensure_config_skeleton_exists()
        main_config = load_main_config()

    if args.name:
        main_config["name"] = args.name[0].strip()

    if args.pronoun:
        main_config["pronoun"] = args.pronoun[0].strip()

    if args.face:
        main_config["catface"] = args.face[0].strip()

    if args.editor:
        main_config["editor"] = args.editor[0].strip()

    save_json(MAIN_CONFIG_FILE, main_config)
    return 0


if __name__ == "__main__":
    main()
