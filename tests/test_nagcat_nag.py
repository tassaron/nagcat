"""Test the integration of nagcat's components in nagcat.main()"""
import os
import tempfile
import shutil
import datetime
from io import StringIO
from contextlib import redirect_stdout

import pytest

import nagcat.nagcat as nagcat
import nagcat.config as config
from test_config import config_dir


@pytest.fixture
def config_dir_and_litterbox_dir(config_dir):
    # Create name of temporary directory for the litterbox
    litterbox_dir = tempfile.mktemp()
    # The test function is responsible for actually creating it
    yield config_dir, litterbox_dir
    # Remove temporary directory after test function
    if os.path.exists(litterbox_dir):
        shutil.rmtree(litterbox_dir)


def test_nagcat_nag_after_reminder(config_dir_and_litterbox_dir):
    # Set current time to 14:00, which is after the default nag
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 15, 14, 0)

    _, litterbox_dir = config_dir_and_litterbox_dir

    # Capture stdout output as a string using StringIO
    with StringIO() as fake_stdout, redirect_stdout(fake_stdout):
        exit_code = nagcat.nagcat_nag(*config.load_all_config(), litterbox_dir)
        output = fake_stdout.getvalue()
    assert exit_code == 0
    assert output == config.MAIN_CONFIG_DEFAULT["alert"]


def test_nagcat_nag_before_reminder(config_dir_and_litterbox_dir):
    # Set current time to 13:59, which is before the default nag
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 15, 13, 59)

    _, litterbox_dir = config_dir_and_litterbox_dir

    # Capture stdout output as a string using StringIO
    with StringIO() as fake_stdout, redirect_stdout(fake_stdout):
        exit_code = nagcat.nagcat_nag(*config.load_all_config(), litterbox_dir)
        output = fake_stdout.getvalue()
    assert exit_code == 0
    assert output == config.MAIN_CONFIG_DEFAULT["face"]
