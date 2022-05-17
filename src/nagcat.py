"""Plain nagcat command, which checks for reminders and prints =^.^= or =u.u="""
from typing import Dict, Optional, Tuple, List
import os
import sys
import argparse
import tempfile
import glob
import re
import string
import shutil
import datetime


def safe_name(name: str) -> str:
    """Make reminder text into a safe filename, trimmed to 40 characters max"""
    return re.sub(f"[{re.escape(string.punctuation)}]", "", name).replace(" ", "_")[:40]


def create_litterbox(litterbox_dir: str) -> bool:
    """Create a litterbox to store the nagcat's data"""
    if not os.path.exists(litterbox_dir):
        os.mkdir(litterbox_dir)
        return True
    return False


def create_text_file(filepath: str, content: str = "") -> None:
    """Creates a string in a text file at filepath"""
    with open(filepath, "w") as f:
        f.write(content)


def get_datetime_now():
    return datetime.datetime.now()


def get_current_time() -> Tuple[int, int]:
    """Return tuple of ints: (hour, minute) in 24-hour time"""
    current_time = get_datetime_now()
    return current_time.hour, current_time.minute


def get_time_from_str(str_time: str) -> Tuple[int, int]:
    """Splits a str such as '14:00' in the constituent hour and minute parts, as a tuple of ints"""
    hour, minute = str_time.split(":")
    return int(hour), int(minute)


def use_litterbox(reminders: Dict[str, str], litterbox_dir: str) -> None:
    """
    Adds reminders to litterbox if they are missing.
    Checks if any daily reminder suffixed with _0 (in the future) is now in the past.
    If any are, then suffix is changed to _1 to indicate a need for nagging.
    """
    for reminder_text in reminders.values():
        # create missing reminders as _0
        reminder_file = os.path.join(litterbox_dir, safe_name(reminder_text))
        if not glob.glob(f"{reminder_file}_*"):
            create_text_file(f"{reminder_file}_0")

    for str_time, reminder_text in reminders.items():
        reminder_file = f"{os.path.join(litterbox_dir, safe_name(reminder_text))}_0"
        if not os.path.exists(reminder_file):
            # should be _1 or _2
            continue
        # Only consider reminders marked as _0 (in future for this day)
        reminder_hour, reminder_minute = get_time_from_str(str_time)
        current_hour, current_minute = get_current_time()
        if reminder_hour < current_hour or (
            reminder_hour == current_hour and reminder_minute <= current_minute
        ):
            os.remove(reminder_file)  # remove _0 file
            reminder_file = f"{os.path.join(litterbox_dir, safe_name(reminder_text))}_1"
            create_text_file(reminder_file, reminder_text)  # create _1 file


def date_has_changed(litterbox_dir: str) -> bool:
    """If litterbox_dir/<current_day> is nonexistent, returns True"""
    current_day = get_datetime_now().day
    datefile = os.path.join(litterbox_dir, str(current_day))
    if not os.path.exists(datefile):
        create_text_file(datefile)
        return True
    return False


def reminders_pending(reminders: Dict[str, str], litterbox_dir: str) -> bool:
    """
    Reminders are put in litterbox, suffixed with numbers to indicate state:
        0 - reminder is in the future on the current day
        1 - reminder is in the past on the current day
        2 - reminder has been "marked as complete" on the current day

    If the current day changes, all reminders get deleted from the litterbox
    """
    if date_has_changed(litterbox_dir):
        dirty_files = glob.glob(os.path.join(litterbox_dir, "*_1"))
        dirty_files.extend(glob.glob(os.path.join(litterbox_dir, "*_2")))
        for reminder in dirty_files:
            os.remove(reminder)

    pending_files_in_litterbox = (
        lambda: len(glob.glob(os.path.join(litterbox_dir, "*_1"))) > 0
    )
    if pending_files_in_litterbox():
        return True

    use_litterbox(reminders, litterbox_dir)
    return pending_files_in_litterbox()


def nagcat_reset(
    main_config: Dict[str, str], litterbox_dir: str, config_dir: str
) -> int:
    """Happens when doing `nagcat --reset` to delete all nagcat configuration and program state"""

    def delete_dir(dir_name: str) -> int:
        try:
            shutil.rmtree(dir_name)
        except FileNotFoundError as e:
            return 1
        return 0

    delete_dir(litterbox_dir)
    errcode = delete_dir(config_dir)
    if errcode:
        return errcode

    if main_config["name"] != "nagcat":
        print(f"{main_config['name']} turned back into nagcat...")
    else:
        print("nagcat reset!")

    return 0


def nagcat_pet(
    main_config: Dict[str, str], reminders: Dict[str, str], litterbox_dir: str
) -> int:
    """Replace all _1 files in the litterbox with _2 files"""
    for reminder_file in glob.glob(os.path.join(litterbox_dir, "*_1")):
        os.remove(reminder_file)
        create_text_file(f"{reminder_file[:-1]}2")
    return 0


def nagcat_why(
    main_config: Dict[str, str], reminders: Dict[str, str], litterbox_dir: str
) -> int:
    """Figures out why nagcat is nagging and prints a cute message"""

    def nagcat_ponder_why() -> Optional[str]:
        """
        Returns a string with the text for the first found reminder _1
        or None if nothing can be found or an error occurs reading the files
        If multiple reminders are found, also mentions the number.
        """
        nonlocal main_config, reminders, litterbox_dir
        dirty_files = glob.glob(os.path.join(litterbox_dir, "*_1"))
        reason = None
        for reminder_file in dirty_files:
            try:
                with open(reminder_file, "r") as f:
                    reason = f.readlines()[0].strip()
                break
            except Exception as e:
                print(e)
                reason = None

        if reason:
            reason = f"{reason} {main_config['face']}"
            if len(dirty_files) > 1:
                reason = f"{reason}\nAnd {len(dirty_files) - 1} more reasons as well..."

        return reason

    why = nagcat_ponder_why()
    if why is not None:
        print(why)
    print(f"{main_config['name']} loves you <3")
    return 0


def nagcat_nag(
    main_config: Dict[str, str], reminders: Dict[str, str], litterbox_dir: str
) -> int:
    """Called when no subcommand is used, therefore does not receive argv as an argument"""

    did_create_new_litterbox = create_litterbox(litterbox_dir)
    if did_create_new_litterbox:
        use_litterbox(reminders, litterbox_dir)

    if reminders_pending(reminders, litterbox_dir):
        print(main_config["alert"], end="")
    else:
        print(main_config["face"], end="")
    return 0


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
    argv: List[str] = sys.argv,
    litterbox_dir: str = os.path.join(tempfile.gettempdir(), "nagcat-litterbox"),
) -> int:
    """
    Entrypoint for nagcat command, `python -m nagcat`, or running nagcat.py directly
    The nagcat "litterbox" is where we keep memory of the current day and reminders
    """
    try:
        from .config import load_all_config, CONFIG_DIR
        from .config import main as config_main
    except ImportError:
        from config import load_all_config, CONFIG_DIR
        from config import main as config_main

    main_config, reminders = load_all_config()
    if len(sys.argv) < 2:
        # Plain nagcat command which returns the 'face' or 'alert'
        return nagcat_nag(main_config, reminders, litterbox_dir)
    elif "--reset" in sys.argv:
        return_code = nagcat_reset(main_config, litterbox_dir, CONFIG_DIR)
        if return_code > 0 or len(sys.argv) == 2:
            return return_code

        main_config, reminders = load_all_config()
        # Remove --reset from argv
        del sys.argv[sys.argv.index("--reset")]

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
