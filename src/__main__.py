"""
Entrypoint for `python -m nagcat` or the nagcat command
"""
import sys

try:
    from .nagcat import main
except ImportError:
    from nagcat import main


if __name__ == "__main__":
    sys.exit(main())
