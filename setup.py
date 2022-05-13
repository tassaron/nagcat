from setuptools import setup, find_packages
from importlib import import_module
from os import path
import re


def getTextFromFile(filename, fallback):
    try:
        with open(
            path.join(path.abspath(path.dirname(__file__)), filename), encoding="utf-8"
        ) as f:
            output = f.read()
    except Exception:
        output = fallback
    return output


PACKAGE_NAME = "nagcat"
SOURCE_DIRECTORY = "src"
SOURCE_PACKAGE_REGEX = re.compile(rf"^{SOURCE_DIRECTORY}")
PACKAGE_DESCRIPTION = "A helpful cat which nags you from within the tmux statusbar... because she loves you! =^.^="


nagcat = import_module(SOURCE_DIRECTORY)
source_packages = find_packages(include=[SOURCE_DIRECTORY, f"{SOURCE_DIRECTORY}.*"])
proj_packages = [
    SOURCE_PACKAGE_REGEX.sub(PACKAGE_NAME, name) for name in source_packages
]


setup(
    name=PACKAGE_NAME,
    version=nagcat.__version__,
    url="https://github.com/tassaron/nagcat",
    description=PACKAGE_DESCRIPTION,
    author=getTextFromFile("AUTHORS", "tassaron"),
    long_description=getTextFromFile("README.md", PACKAGE_DESCRIPTION),
    long_description_content_type = "text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=[
        "reminder",
        "cat",
    ],
    packages=proj_packages,
    package_dir={PACKAGE_NAME: SOURCE_DIRECTORY},
    entry_points={
        "console_scripts": [f"{PACKAGE_NAME} = {PACKAGE_NAME}.__main__:main"],
    },
    scripts=["nagcat.tmux"],
)
