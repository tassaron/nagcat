"""Always runs when importing nagcat package"""
import os
import tempfile

TMP_DIR = os.path.join(tempfile.gettempdir(), "nagcat-litterbox")

__version__ = "1.0.0"
