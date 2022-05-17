"""Test of nagcat_pet function"""
import os
import datetime
import glob

import nagcat.nagcat as nagcat
from test_config import config_dir
from test_nagcat import config_and_litterbox


def test_nagcat_pet(config_and_litterbox):
    nagcat.get_datetime_now = lambda: datetime.datetime(2022, 5, 15, 14)
    main_config, reminders, litterbox_dir = config_and_litterbox
    nagcat.use_litterbox(reminders, litterbox_dir)
    
    assert len(glob.glob(os.path.join(litterbox_dir, "*_1"))) == 1
    assert len(glob.glob(os.path.join(litterbox_dir, "*_2"))) == 0
    
    nagcat.nagcat_pet(main_config, reminders, litterbox_dir)
    
    assert len(glob.glob(os.path.join(litterbox_dir, "*_1"))) == 0
    assert len(glob.glob(os.path.join(litterbox_dir, "*_2"))) == 1
