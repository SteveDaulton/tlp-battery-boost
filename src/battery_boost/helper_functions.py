"""Miscellaneous helper functions for battery boost."""
import argparse
import importlib
import shutil
from collections import defaultdict
from tkinter import messagebox
from typing import TypeAlias

from battery_boost.constants import THEME, ThemeName, FONT_SIZES, ThemeKeys


def check_tlp_installed() -> bool:
    """Verify TLP is available.

    Returns:
        bool: True if TLP is installed; False otherwise. Displays an error
        dialog if not found.
    """
    if not shutil.which('tlp'):
        messagebox.showerror("Error", "TLP is not installed or not in PATH.")
        return False
    return True


def format_battery_str(name: str, info: defaultdict[str, str]) -> str:
    """Return parsed battery data as a human-readable block of text."""
    return (f"{name}:\n"
            f"  Start threshold: {info['start']}%\n"
            f"  End threshold: {info['end']}%\n"
            f"  Current Charge: {info['charge']}% "
            f"of {info['capacity']}%\n")


Config: TypeAlias = tuple[ThemeKeys, tuple[str, int], tuple[str, int], float]


def parse_args(argv: list[str]) -> Config:
    """Return tuple (theme_dict, font_normal, font_small)"""
    parser = argparse.ArgumentParser(
        description="A simple GUI to enable `tlp fullcharge`.",
        # Automatically add defaults to help text.
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    version = importlib.metadata.version("tlp-battery-boost")
    parser.add_argument('-v', '--version',
                        action='version',
                        version=f"Battery Boost {version}")

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
