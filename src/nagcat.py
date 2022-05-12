"""Plain nagcat command, which checks for reminders and prints =^.^= or [!!!]"""
from typing import Dict
import os
import tempfile

from . import logger


TMP_DIR = os.path.join("nagcat-litterbox-", tempfile.gettempdir())


def create_litterbox():
    """Create a litterbox to store the nagcat's data"""
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)


def main(main_config: Dict[str, str], reminders: Dict[str, str]) -> int:
    """Called when no subcommand is used, therefore does not receive argv as an argument"""
    print(main_config["catface"], end="")
    return 0


if __name__ == "__main__":
    from .config import load_all_config

    main(*load_all_config())
