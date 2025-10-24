"""Wrappers for executing TLP system commands in a Tkinter context.

Provides functions to initialize, toggle, and query TLP using sudo,
with error handling suitable for a GUI application.
"""

from __future__ import annotations

import subprocess
from tkinter import messagebox
from typing import TYPE_CHECKING

from battery_boost.constants import BatteryState

if TYPE_CHECKING:
    from battery_boost.app import App


def initialise_tlp(_parent: App) -> None:
    """Initialize TLP to the default state.

    Runs `sudo tlp start` to reset configuration. Shows an error dialog and exits
    if the command fails.
    """
    try:
        subprocess.run(['sudo', 'tlp', 'start'], check=True)
        return

    except Exception as exc:  # pylint: disable=broad-exception-caught
        messagebox.showerror("Unexpected Error",
                             f"Could not initialize TLP.\n{exc}",
                             parent=_parent)
        _parent.quit_app(f"Error: Could not initialize TLP: {exc}")


def tlp_toggle_state(_parent: App, current_state: BatteryState) -> None:
    """Toggle TLP between default and full-charge profiles.

    Args:
        _parent: The Tkinter app instance, used for error dialogs.
        current_state: The current battery profile.
    """
    try:
        if current_state == BatteryState.DEFAULT:
            subprocess.run(['sudo', 'tlp', 'fullcharge'], check=True)
        else:
            subprocess.run(['sudo', 'tlp', 'start'], check=True)
    except subprocess.CalledProcessError as exc:
        _parent.quit_on_error(f"TLP command failed: {exc.returncode}:\n"
                              f"{exc.stderr or exc}")
    except FileNotFoundError as exc:
        _parent.quit_on_error(f"Command not found: {exc.filename}")
    except OSError as exc:
        _parent.quit_on_error(f"System error while running TLP command: {exc}")


def tlp_get_stats() -> str:
    """Retrieve TLP battery statistics.

    Runs `sudo tlp-stat -b` and returns stdout. Returns an error message string
    if the command fails.
    """
    try:
        result = subprocess.run(['sudo', 'tlp-stat', '-b'],
                                text=True,
                                capture_output=True,
                                check=True)
    except subprocess.CalledProcessError as exc:
        return f"Error: Failed to run tlp-stat:\n{exc.stderr or exc}"
    except OSError as exc:
        return f"Error: System error while running tlp-stat: {exc}"
    except Exception as exc:  # pylint: disable=broad-exception-caught
        return f"Error: Unexpected error: {exc}"
    return result.stdout
