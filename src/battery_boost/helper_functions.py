"""Helper functions for Battery Boost."""

import argparse
from importlib.metadata import version
import shutil
from pathlib import Path
from typing import TypeAlias

from battery_boost.constants import THEME, ThemeName, FONT_SIZES, ThemeKeys
from battery_boost.shell_commands import TlpCommandError, tlp_get_stats
from battery_boost.tlp_parser import parse_tlp_stats


def command_on_path(command: str) -> bool:
    """Return True if command is available in PATH, else False."""
    return bool(shutil.which(command))


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


def on_ac_power() -> bool:
    """Return True if on AC power, else False."""
    base = Path("/sys/class/power_supply")
    if not Path.is_dir(base):
        # Unsupported system
        raise RuntimeError("Power supply information not available.")

    for child in base.iterdir():
        online_file = child / "online"
        if online_file.is_file():
            try:
                return online_file.read_text().strip() == "1"
            except OSError:
                pass

    return False


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
