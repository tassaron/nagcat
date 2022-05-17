"""Test of nagcat_pet function"""
import datetime
from io import StringIO
from contextlib import redirect_stdout

import nagcat.nagcat as nagcat
import nagcat.config as config
from test_config import config_dir
from test_reminders import config_and_litterbox


def test_nagcat_why(config_and_litterbox):
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 15, 14)
    main_config, reminders, litterbox_dir = config_and_litterbox
    nagcat.use_litterbox(reminders, litterbox_dir)

    # Capture stdout output as a string using StringIO
    with StringIO() as fake_stdout, redirect_stdout(fake_stdout):
        exit_code = nagcat.nagcat_why(main_config, reminders, litterbox_dir)
        output = fake_stdout.getvalue()
        
    assert exit_code == 0
    assert config.REMINDERS_CONFIG_DEFAULT["14:00"] in output
