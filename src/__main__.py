"""
Entrypoint for `python -m nagcat` or the nagcat command
"""
import sys
import argparse

from .config import load_all_config, load_main_config
from .config import main as config_main

from . import log


def create_argparser():
    main_config = load_main_config()
    parser = argparse.ArgumentParser(
        description="A helpful cat which nags you from within the tmux statusbar... because she loves you!",
        epilog=main_config["catface"],
    )
    parser.add_argument(
        "suggestion",
        help=f"suggest something for {main_config['name']} to do",
        choices=["config"],
    )

    return parser


def main() -> int:
    if len(sys.argv) < 2:
        # plain nagcat command, used by tmux or manual refresh
        main_config, reminders = load_all_config()
        print(main_config["catface"], end="")
        return 0

    parser = create_argparser()
    # parse only the suggestion to begin with
    args = parser.parse_args(sys.argv[1:2])

    if args.suggestion == "config":
        return config_main()

    return 1


if __name__ == "__main__":
    sys.exit(main())
