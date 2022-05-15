"""
Entrypoint for `python -m nagcat` or the nagcat command
"""
import os
import sys
import argparse
import tempfile
from typing import Dict

from .config import load_all_config, CONFIG_DIR
from .config import main as config_main
from .nagcat import nagcat_why, nagcat_pet, nagcat_reset
from .nagcat import main as nagcat_main


def create_argparser(main_config: Dict[str, str]) -> argparse.ArgumentParser:
    """Create and return an argparser for this command entrypoint"""
    parser = argparse.ArgumentParser(
        description=f"{main_config['name']}, who nags you from within the tmux statusbar..."
        f"because {main_config['pronoun']} love{'s' if main_config['pronoun'] != 'they' else ''} you!",
        epilog=main_config["face"],
    )
    parser.add_argument(
        "suggestion",
        help=f"suggest something for {main_config['name']} to do",
        choices=["config", "pet", "why"],
    )
    parser.add_argument(
        "--reset",
        help="delete all config files and reminder state",
        action="store_true",
    )

    return parser


def main(
    litterbox_dir: str = os.path.join(tempfile.gettempdir(), "nagcat-litterbox")
) -> int:
    """
    Entrypoint when running nagcat as a module, i.e., `python -m nagcat`
    The nagcat "litterbox" is where we keep memory of the current day and reminders
    """
    main_config, reminders = load_all_config()
    if len(sys.argv) < 2:
        # Plain nagcat command which returns the 'face' or 'alert'
        return nagcat_main(main_config, reminders, litterbox_dir)
    elif sys.argv[1] == "--reset":
        return_code = nagcat_reset(main_config, litterbox_dir, CONFIG_DIR)
        if return_code > 0 or len(sys.argv) == 2:
            return return_code

        main_config, reminders = load_all_config()
        # Remove --reset from argv
        sys.argv = sys.argv[1:]

    parser = create_argparser(main_config)
    # Parse only the suggestion to begin with
    args = parser.parse_args(sys.argv[1:2])

    # At this point argparse has returned 1 or higher if args are bad

    if args.suggestion == "config":
        # pass remaining arguments into config subcommand
        return config_main(sys.argv[2:], litterbox_dir)

    elif args.suggestion == "pet":
        return nagcat_pet(main_config, reminders, litterbox_dir)

    elif args.suggestion == "why":
        return nagcat_why(main_config, reminders, litterbox_dir)

    # This should never occur, as argparse returned 1 above
    raise NotImplementedError


if __name__ == "__main__":
    exit(main())
