"""Helper functions for Battery Boost."""

import argparse
from importlib.metadata import version
import shutil
from typing import TypeAlias

from battery_boost.constants import THEME, ThemeName, FONT_SIZES, ThemeKeys
from battery_boost.tlp_command import TlpCommandError, tlp_get_stats
from battery_boost.tlp_parser import parse_tlp_stats


def check_tlp_installed() -> bool:
    """Return True if TLP is installed and available in PATH, else False."""
    return bool(shutil.which('tlp'))


def get_battery_stats(action: str) -> str:
    """Retrieve raw statistics from battery.

    Returns:
        Formatted statistics or error message as a string.
    """
    try:
        raw_stats = tlp_get_stats()
        parsed = parse_tlp_stats(raw_stats)
        return f"{action}{parsed}"
    except TlpCommandError as exc:
        return f"Error: {exc}"


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
