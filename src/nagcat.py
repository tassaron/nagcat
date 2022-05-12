"""Plain nagcat command, which checks for reminders and prints =^.^= or [!!!]"""
from typing import Dict, Tuple
import os
import tempfile
import glob
import re
import string
import datetime

from . import logger


TMP_DIR = os.path.join(tempfile.gettempdir(), "nagcat-litterbox")


def safe_name(name) -> str:
    """Make reminder text into a safe filename, trimmed to 40 characters max"""
    return re.sub(f"[{re.escape(string.punctuation)}]", "", name).replace(" ", "_")[:40]


def create_litterbox() -> bool:
    """Create a litterbox to store the nagcat's data"""
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)
        return True
    return False


def create_text_file(filepath) -> None:
    """Creates an empty text file at filepath"""
    with open(filepath, "w") as f:
        f.write("")


def get_current_time() -> Tuple[int, int]:
    current_time = datetime.datetime.now()
    return current_time.hour, current_time.minute


def get_time_from_str(str_time: str) -> Tuple[int, int]:
    hour, minute = str_time.split(":")
    return int(hour), int(minute)


def use_litterbox(reminders: Dict[str, str]) -> None:
    """
    Adds reminders to litterbox if they are missing.
    Checks if any daily reminder suffixed with _0 (in the future) is now in the past.
    If any are, then suffix is changed to _1 to indicate a need for nagging.
    """
    logger.info("Using litterbox")
    for reminder_text in reminders.values():
        # create missing reminders as _0
        reminder_file = os.path.join(TMP_DIR, safe_name(reminder_text))
        if not glob.glob(f"{reminder_file}_*"):
            create_text_file(f"{reminder_file}_0")

    for str_time, reminder_text in reminders.items():
        reminder_file = f"{os.path.join(TMP_DIR, safe_name(reminder_text))}_0"
        if not os.path.exists(reminder_file):
            # should be _1 or _2
            continue
        # Only consider reminders marked as _0 (in future for this day)
        reminder_hour, reminder_minute = get_time_from_str(str_time)
        current_hour, current_minute = get_current_time()
        if reminder_hour < current_hour or (
            reminder_hour == current_hour and reminder_minute < current_minute
        ):
            os.remove(reminder_file)  # remove _0 file
            reminder_file = f"{os.path.join(TMP_DIR, safe_name(reminder_text))}_1"
            create_text_file(reminder_file)  # create _1 file


def date_has_changed() -> bool:
    """If TMP_DIR/<current_day> is nonexistent, returns True"""
    current_day = datetime.datetime.now().day
    datefile = os.path.join(TMP_DIR, str(current_day))
    if not os.path.exists(datefile):
        create_text_file(datefile)
        return True
    return False


def reminders_pending(reminders: Dict[str, str]) -> bool:
    """
    Reminders are put in litterbox, suffixed with numbers to indicate state:
        0 - reminder is in the future on the current day
        1 - reminder is in the past on the current day
        2 - reminder has been "marked as complete" on the current day

    If the current day changes, all reminders get deleted from the litterbox
    """
    if date_has_changed():
        dirty_files = glob.glob(os.path.join(TMP_DIR, "*_1"))
        dirty_files.extend(glob.glob(os.path.join(TMP_DIR, "*_2")))
        for reminder in dirty_files:
            os.remove(reminder)

    pending_files_in_litterbox = (
        lambda: len(glob.glob(os.path.join(TMP_DIR, "*_1"))) > 0
    )
    if pending_files_in_litterbox():
        return True

    use_litterbox(reminders)
    return pending_files_in_litterbox()


def nagcat_pet(main_config: Dict[str, str], reminders: Dict[str, str]) -> int:
    """Replace all _1 files in the litterbox with _2 files"""
    for reminder_file in glob.glob(os.path.join(TMP_DIR, "*_1")):
        os.remove(reminder_file)
        create_text_file(f"{reminder_file[:-1]}2")
    return 0


def nagcat_why(main_config: Dict[str, str], reminders: Dict[str, str]) -> int:
    print("idk!")
    return 0


def main(main_config: Dict[str, str], reminders: Dict[str, str]) -> int:
    """Called when no subcommand is used, therefore does not receive argv as an argument"""

    did_create_new_litterbox = create_litterbox()
    if did_create_new_litterbox:
        use_litterbox(reminders)

    if reminders_pending(reminders):
        print("[!!!]", end="")
    else:
        print(main_config["catface"], end="")
    return 0


if __name__ == "__main__":
    from .config import load_all_config

    main(*load_all_config())
