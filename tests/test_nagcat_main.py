"""Test the integration of nagcat's components in nagcat.main()"""
import os
import sys
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
def config_and_litterbox(config_dir):
    # Create name of temporary directory for the litterbox
    litterbox_dir = tempfile.mktemp()
    # The test function is responsible for actually creating it
    yield config_dir, litterbox_dir
    # Remove temporary directory after test function
    if os.path.exists(litterbox_dir):
        shutil.rmtree(litterbox_dir)


def test_nagcat_main_after_nag(config_and_litterbox):
    # Set current time to 14:00
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 15, 14, 1)

    _, litterbox_dir = config_and_litterbox
    
    # Capture stdout output as a string using StringIO
    with StringIO() as fake_stdout, redirect_stdout(fake_stdout):
        exit_code = nagcat.main(*config.load_all_config(), litterbox_dir)
        output = fake_stdout.getvalue()
    assert exit_code == 0
    assert output == config.MAIN_CONFIG_DEFAULT["alert"]


def test_nagcat_main_before_nag(config_and_litterbox):
    # Set current time to 9:00
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 15, 9)

    _, litterbox_dir = config_and_litterbox

    # Capture stdout output as a string using StringIO
    with StringIO() as fake_stdout, redirect_stdout(fake_stdout):
        exit_code = nagcat.main(*config.load_all_config(), litterbox_dir)
        output = fake_stdout.getvalue()
    assert exit_code == 0
    assert output == config.MAIN_CONFIG_DEFAULT["face"]
