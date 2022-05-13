"""
Entrypoint for `python -m nagcat` or the nagcat command
"""
import sys
import argparse
from typing import Dict

from .config import load_all_config
from .config import main as config_main
from .nagcat import nagcat_why, nagcat_pet
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

    return parser


def main() -> int:
    main_config, reminders = load_all_config()
    if len(sys.argv) < 2:
        # plain nagcat command, used by tmux or manual refresh
        return nagcat_main(main_config, reminders)

    parser = create_argparser(main_config)
    # parse only the suggestion to begin with
    args = parser.parse_args(sys.argv[1:2])

    if args.suggestion == "config":
        # pass remaining arguments into config subcommand
        return config_main(sys.argv[2:])

    elif args.suggestion == "pet":
        return nagcat_pet(main_config, reminders)

    elif args.suggestion == "why":
        return nagcat_why(main_config, reminders)

    return 1


if __name__ == "__main__":
    sys.exit(main())
