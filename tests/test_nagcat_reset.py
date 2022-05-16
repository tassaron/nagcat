"""Test of nagcat_reset function"""
import os

import nagcat.nagcat as nagcat
import nagcat.config as config
from test_config import config_dir
from test_nagcat_main import config_dir_and_litterbox_dir


def test_nagcat_reset_all(config_dir_and_litterbox_dir):
    config_dir, litterbox_dir = config_dir_and_litterbox_dir
    main_config, _ = config.load_all_config()
    nagcat.create_litterbox(litterbox_dir)

    assert os.path.exists(config_dir)
    assert os.path.exists(litterbox_dir)

    exit_code = nagcat.nagcat_reset(main_config, litterbox_dir, config_dir)

    assert exit_code == 0
    assert not os.path.exists(config_dir)
    assert not os.path.exists(litterbox_dir)


def test_nagcat_reset_without_litterbox(config_dir_and_litterbox_dir):
    config_dir, litterbox_dir = config_dir_and_litterbox_dir
    main_config, _ = config.load_all_config()

    assert os.path.exists(config_dir)
    assert not os.path.exists(litterbox_dir)

    exit_code = nagcat.nagcat_reset(main_config, litterbox_dir, config_dir)

    assert exit_code == 0
    assert not os.path.exists(config_dir)
    assert not os.path.exists(litterbox_dir)


def test_nagcat_reset_without_config(config_dir_and_litterbox_dir):
    config_dir, litterbox_dir = config_dir_and_litterbox_dir
    nagcat.create_litterbox(litterbox_dir)

    assert not os.path.exists(config_dir)
    assert os.path.exists(litterbox_dir)

    exit_code = nagcat.nagcat_reset(config.MAIN_CONFIG_DEFAULT, litterbox_dir, config_dir)

    assert exit_code == 1
    assert not os.path.exists(litterbox_dir)


def test_nagcat_reset_without_all(config_dir_and_litterbox_dir):
    config_dir, litterbox_dir = config_dir_and_litterbox_dir
    assert not os.path.exists(config_dir)
    assert not os.path.exists(litterbox_dir)

    exit_code = nagcat.nagcat_reset(config.MAIN_CONFIG_DEFAULT, litterbox_dir, config_dir)

    assert exit_code == 1
