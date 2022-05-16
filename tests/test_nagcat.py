import os
import tempfile
import shutil
import datetime
import glob

import pytest

import nagcat.nagcat as nagcat
import nagcat.config as config
from test_config import config_dir
from test_litterbox import litterbox_dir


@pytest.fixture
def config_and_litterbox(config_dir):
    # Create name of temporary directory for the litterbox
    litterbox_dir = tempfile.mktemp()
    nagcat.create_litterbox(litterbox_dir)
    yield *config.load_all_config(), litterbox_dir
    # Remove temporary directory after test function
    if os.path.exists(litterbox_dir):
        shutil.rmtree(litterbox_dir)


def test_date_has_changed(litterbox_dir):
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 15)
    success = nagcat.date_has_changed(litterbox_dir)
    assert success
    success = nagcat.date_has_changed(litterbox_dir)
    assert not success

    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 16)
    success = nagcat.date_has_changed(litterbox_dir)
    assert success


def test_use_litterbox(config_and_litterbox):
    _, reminders, litterbox_dir = config_and_litterbox
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 15, 9)
    assert len(glob.glob(os.path.join(litterbox_dir, "*_0"))) == 0
    nagcat.use_litterbox(reminders, litterbox_dir)
    assert len(glob.glob(os.path.join(litterbox_dir, "*_0"))) == 1


def test_reminders_pending_midday(config_and_litterbox):
    _, reminders, litterbox_dir = config_and_litterbox
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 15)
    nagcat.use_litterbox(reminders, litterbox_dir)
    assert not nagcat.reminders_pending(reminders, litterbox_dir)
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 15, 14)
    nagcat.use_litterbox(reminders, litterbox_dir)
    assert nagcat.reminders_pending(reminders, litterbox_dir)


def test_reminders_pending_overnight(config_and_litterbox):
    _, reminders, litterbox_dir = config_and_litterbox
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 15, 23)
    nagcat.use_litterbox(reminders, litterbox_dir)
    assert nagcat.reminders_pending(reminders, litterbox_dir)
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 16, 0)
    nagcat.use_litterbox(reminders, litterbox_dir)
    assert not nagcat.reminders_pending(reminders, litterbox_dir)
