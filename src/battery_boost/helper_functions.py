"""Helper functions for Battery Boost."""

import argparse
from importlib.metadata import version
import shutil
from tkinter import messagebox
from typing import TypeAlias

from battery_boost.constants import THEME, ThemeName, FONT_SIZES, ThemeKeys


def check_tlp_installed() -> bool:
    """Check whether TLP is installed and available in PATH.

    Returns:
        bool: True if TLP is found, False otherwise. Shows an error dialog if not found.
    """
    if not shutil.which('tlp'):
        messagebox.showerror("Error", "TLP is not installed or not in PATH.")
        return False
    return True


Config: TypeAlias = tuple[ThemeKeys, tuple[str, int], tuple[str, int], float]


def parse_args(argv: list[str]) -> Config:
    """Parse command-line arguments and return configuration.

    Args:
        argv: List of command-line arguments.

    Returns:
        tuple: (theme_dict, standard_font, small_font, scale_factor).
    """
    parser = argparse.ArgumentParser(
        description="A simple GUI to enable `tlp fullcharge`.",
        # Automatically add defaults to help text.
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-v', '--version',
                        action='version',
                        version=f"Battery Boost {version('tlp-battery-boost')}")

    parser.add_argument(
        '-f', '--font-size',
        type=int,
        choices=range(1, 6),
        default=3,
        metavar="{1-5}",
        help="Font size [1-5] (1=smallest, 5=largest)")

    parser.add_argument(
        '-t', '--theme',
        choices=['light', 'dark'],
        default='light',
        help="Color theme",)

    parsed_args = parser.parse_args(argv)
    standard_font, small_font, scale_factor = FONT_SIZES[parsed_args.font_size]
    return THEME[ThemeName(parsed_args.theme)], standard_font, small_font, scale_factor
