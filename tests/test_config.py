import os
import tempfile
import shutil
import pytest

import nagcat.config as config


@pytest.fixture
def config_dir():
    # Create a temporary directory to serve as a fake "Home folder"
    fake_home_dir = tempfile.mkdtemp()

    # Set global variables involving CONFIG_DIR to our temporary directory
    # Do not create the config dirs yet. That is nagcat's job
    config.CONFIG_DIR = os.path.join(fake_home_dir, "test-config")
    config.MAIN_CONFIG_FILE = os.path.join(config.CONFIG_DIR, "test-nagcat.json")
    config.REMINDERS_CONFIG_FILE = os.path.join(
        config.CONFIG_DIR, "test-reminders.json"
    )
    # Return to function receiving fixture
    yield config.CONFIG_DIR

    # Remove temporary directory after test function
    shutil.rmtree(fake_home_dir)


def test_ensure_config_skeleton_exists(config_dir):
    assert not os.path.exists(config.CONFIG_DIR)
    config.ensure_config_skeleton_exists()
    assert config.get_json(config.MAIN_CONFIG_FILE) == config.MAIN_CONFIG_DEFAULT


def test_add_default_values_to_json():
    test_data = {"name": "Rosie"}
    test_data, mutated = config.add_default_values_to_json(
        config.MAIN_CONFIG_DEFAULT, test_data
    )
    assert mutated == True
    assert len(test_data) == len(config.MAIN_CONFIG_DEFAULT)
    assert test_data["name"] == "Rosie"
