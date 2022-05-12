"""
Entrypoint for `python -m nagcat` or the nagcat command
"""
import sys
import argparse

from .config import load_all_config, load_main_config
from .config import main as config_main
from .nagcat import main as nagcat_main
from . import logger


def create_argparser() -> argparse.ArgumentParser:
    """Create and return an argparser for this command entrypoint"""
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
        return nagcat_main(*load_all_config())

    parser = create_argparser()
    # parse only the suggestion to begin with
    args = parser.parse_args(sys.argv[1:2])

    # pass remaining arguments into subcommands
    if args.suggestion == "config":
        return config_main(sys.argv[2:])

    return 1


if __name__ == "__main__":
    sys.exit(main())
