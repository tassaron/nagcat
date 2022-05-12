"""
Entrypoint for `python -m nagcat` or the nagcat command
"""
import sys
import logging
import argparse

from .config import load_config
from .config import main as config_main


log = logging.getLogger(__package__)


def create_argparser():
    parser = argparse.ArgumentParser(
        description="A helpful cat which nags you from within the tmux statusbar... because she loves you!",
        epilog="=^.^=",
    )
    parser.add_argument(
        "suggestion", help="suggest something for nagcat to do", choices=["config"]
    )

    return parser


def main():
    parser = create_argparser()
    # parse only the suggestion to begin with
    args = parser.parse_args(sys.argv[1:2])

    if args.suggestion == "config":
        config_main()


if __name__ == "__main__":
    main()
