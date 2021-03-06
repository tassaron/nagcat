"""Test nagcat litterbox functions"""
import os
import tempfile
import shutil
import datetime

import pytest

import nagcat.nagcat as nagcat


@pytest.fixture
def litterbox_dir():
    # Create name of temporary directory for the litterbox
    litterbox_dir = tempfile.mktemp()
    nagcat.create_litterbox(litterbox_dir)
    yield litterbox_dir
    # Remove temporary directory after test function
    shutil.rmtree(litterbox_dir)


def test_create_litterbox():
    litterbox_dir = tempfile.mktemp()
    success = nagcat.create_litterbox(litterbox_dir)
    assert success
    assert os.path.exists(litterbox_dir)
    shutil.rmtree(litterbox_dir)


def test_create_text_file(litterbox_dir):
    test_file = os.path.join(litterbox_dir, "test_text")
    nagcat.create_text_file(test_file, "test text")
    with open(test_file, "r") as f:
        content = f.readlines()[0].strip()
    assert content == "test text"


def test_date_has_changed(litterbox_dir):
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 15)
    success = nagcat.date_has_changed(litterbox_dir)
    assert success
    success = nagcat.date_has_changed(litterbox_dir)
    assert not success

    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 16)
    success = nagcat.date_has_changed(litterbox_dir)
    assert success