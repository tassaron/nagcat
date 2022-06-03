import os
import tempfile
import shutil
import datetime
import glob

import pytest

import nagcat.nagcat as nagcat
import nagcat.config as config
from test_config import config_dir


@pytest.fixture
def config_and_litterbox(config_dir):
    # Create name of temporary directory for the litterbox
    litterbox_dir = tempfile.mktemp()
    nagcat.create_litterbox(litterbox_dir)
    yield *config.load_all_config(), litterbox_dir
    # Remove temporary directory after test function
    if os.path.exists(litterbox_dir):
        shutil.rmtree(litterbox_dir)


def test_use_litterbox(config_and_litterbox):
    _, reminders, litterbox_dir = config_and_litterbox
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 15, 9)
    assert len(glob.glob(os.path.join(litterbox_dir, "*_0"))) == 0
    nagcat.use_litterbox(reminders, litterbox_dir)
    assert len(glob.glob(os.path.join(litterbox_dir, "*_0"))) == 1


def test_reminder_not_pending_same_day(config_and_litterbox):
    """Reminder for 14:00 is not pending before 14:00 on same day"""
    _, reminders, litterbox_dir = config_and_litterbox
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 15)
    nagcat.use_litterbox(reminders, litterbox_dir)
    assert not nagcat.reminders_pending(reminders, litterbox_dir)


def test_reminder_pending_same_day(config_and_litterbox):
    """Reminder for 14:00 is pending after 14:00 on same day"""
    _, reminders, litterbox_dir = config_and_litterbox
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 15)
    nagcat.use_litterbox(reminders, litterbox_dir)
    assert not nagcat.reminders_pending(reminders, litterbox_dir)
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 15, 14)
    nagcat.use_litterbox(reminders, litterbox_dir)
    assert nagcat.reminders_pending(reminders, litterbox_dir)


def test_reminder_pending_tomorrow(config_and_litterbox):
    """Reminder for 14:00 is pending after 14:00 after 1 day"""
    _, reminders, litterbox_dir = config_and_litterbox
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 15, 23)
    nagcat.use_litterbox(reminders, litterbox_dir)
    assert nagcat.reminders_pending(reminders, litterbox_dir)
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 16, 14)
    nagcat.use_litterbox(reminders, litterbox_dir)
    assert nagcat.reminders_pending(reminders, litterbox_dir)


def test_reminder_not_pending_tomorrow(config_and_litterbox):
    """Reminder for 14:00 is not pending before 14:00 after 1 day"""
    _, reminders, litterbox_dir = config_and_litterbox
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 15, 23)
    nagcat.use_litterbox(reminders, litterbox_dir)
    assert nagcat.reminders_pending(reminders, litterbox_dir)
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 16)
    nagcat.use_litterbox(reminders, litterbox_dir)
    assert not nagcat.reminders_pending(reminders, litterbox_dir)


def test_reminder_pending_after_two_days(config_and_litterbox):
    """Reminder for 14:00 is pending after 14:00 after 2 days"""
    _, reminders, litterbox_dir = config_and_litterbox
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 15, 23)
    nagcat.use_litterbox(reminders, litterbox_dir)
    assert nagcat.reminders_pending(reminders, litterbox_dir)
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 17, 14)
    nagcat.use_litterbox(reminders, litterbox_dir)
    assert nagcat.reminders_pending(reminders, litterbox_dir)


def test_reminder_not_pending_after_two_days(config_and_litterbox):
    """Reminder for 14:00 is not pending before 14:00 after 2 days"""
    _, reminders, litterbox_dir = config_and_litterbox
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 15, 23)
    nagcat.use_litterbox(reminders, litterbox_dir)
    assert nagcat.reminders_pending(reminders, litterbox_dir)
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 17, 0)
    nagcat.use_litterbox(reminders, litterbox_dir)
    assert not nagcat.reminders_pending(reminders, litterbox_dir)
