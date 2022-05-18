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


nagcat = import_module(SOURCE_DIRECTORY)
source_packages = find_packages(include=[SOURCE_DIRECTORY, f"{SOURCE_DIRECTORY}.*"])
proj_packages = [
    SOURCE_PACKAGE_REGEX.sub(PACKAGE_NAME, name) for name in source_packages
]


setup(
    name=PACKAGE_NAME,
    version=nagcat.__version__,
    url="https://github.com/tassaron/nagcat",
    description=nagcat.__doc__,
    author=getTextFromFile("AUTHORS", "tassaron"),
    author_email="brianna@rainey.tech",
    long_description=getTextFromFile("README.md", nagcat.__doc__),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.10",
        "Environment :: Console",
    ],
    keywords=[
        "tmux",
        "reminder",
        "cat",
    ],
    license="MIT",
    packages=proj_packages,
    package_dir={PACKAGE_NAME: SOURCE_DIRECTORY},
    entry_points={
        "console_scripts": [f"{PACKAGE_NAME} = {PACKAGE_NAME}.__main__:main"],
    },
    scripts=["nagcat.tmux"],
)
