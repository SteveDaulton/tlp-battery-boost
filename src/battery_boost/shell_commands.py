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


_TIMEOUT = 5  # All subprocess calls expected to be fast.


class TlpCommandError(Exception):
    """Raised when tlp-stat fails to run properly."""


def tlp_active() -> bool:
    """Return True if TLP is installed, enabled, and has run recently."""
    try:
        result = subprocess.run(
            ["tlp-stat", "-s"],
            capture_output=True,
            text=True,
            check=False,  # don't raise if tlp-stat exits nonzero
            timeout=_TIMEOUT
        )
        output = result.stdout
        state_enabled = False
        last_run_valid = False

        for line in output.splitlines():
            line = line.strip().lower()
            if line.startswith("state") and 'enabled' in line:
                state_enabled = True
            if line.startswith("last run") and 'n/a' not in line:
                last_run_valid = True
        return state_enabled and last_run_valid
    except (subprocess.SubprocessError,
            FileNotFoundError,
            UnicodeDecodeError,
            subprocess.TimeoutExpired):
        return False


def initialise_tlp(_parent: App) -> None:
    """Initialize TLP to the default state.

    Runs `sudo tlp start` to reset configuration. Shows an error dialog and exits
    if the command fails.
    """
    try:
        subprocess.run(['sudo', 'tlp', 'start'], check=True, timeout=_TIMEOUT)
        return

    except Exception as exc:  # pylint: disable=broad-exception-caught
        messagebox.showerror("TLP Command Error",
                             f"Could not initialize TLP.\n{exc}",
                             parent=_parent)
        _parent.quit_app(f"Error: Could not initialize TLP: {exc}")


def tlp_toggle_state(_parent: App, current_state: BatteryState) -> bool:
    """Toggle TLP between default and full-charge profiles.

    Args:
        _parent: The Tkinter api instance, used for error dialogs.
        current_state: The current battery profile.
    Returns:
        True if successful, False otherwise.
    """
    try:
        if current_state == BatteryState.DEFAULT:
            subprocess.run(['sudo', 'tlp', 'fullcharge'],
                           check=True,
                           capture_output=True,
                           timeout=_TIMEOUT)
        else:
            subprocess.run(['sudo', 'tlp', 'start'],
                           check=True,
                           capture_output=True,
                           timeout=_TIMEOUT)
    except FileNotFoundError as exc:
        _parent.quit_on_error(f"Command not found: {exc.filename}",
                              "TLP Command Error")
    except subprocess.CalledProcessError as exc:
        # Special case: fullcharge requires AC power.
        if not _parent.ensure_ac_power():
            return False  # Non-fatal failure

        _parent.quit_on_error(f"TLP command failed: {exc.returncode}:\n"
                              f"{exc.stderr or exc}",
                              "TLP Command Error")

    except (OSError, subprocess.TimeoutExpired) as exc:
        _parent.quit_on_error(f"System error while running TLP command: {exc}",
                              "TLP Command Error")
    return True


def tlp_get_stats() -> str:
    """Retrieve TLP battery statistics.

    Runs `sudo tlp-stat -b` and returns stdout.

    Raises:
        TlpCommandError: Exception if the command fails.
    """
    try:
        result = subprocess.run(['sudo', 'tlp-stat', '-b'],
                                text=True,
                                capture_output=True,
                                check=True,
                                timeout=_TIMEOUT)
    # pylint: disable=raise-missing-from
    except subprocess.CalledProcessError as exc:
        raise TlpCommandError(f"Failed to run tlp-stat:\n{exc.stderr or exc}")
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise TlpCommandError(f"System error while running tlp-stat: {exc}")
    except Exception as exc:  # pylint: disable=broad-exception-caught
        raise TlpCommandError(f"Unexpected error: {exc}")
    return result.stdout


def tlp_running() -> bool:
    """Return True if TLP is running, else False."""
    try:
        result = subprocess.run(['systemctl', 'is-active', 'tlp.service'],
                                capture_output=True,
                                text=True,
                                check=True,
                                timeout=_TIMEOUT)
        return result.stdout.strip() == 'active'
    except (subprocess.CalledProcessError,
            subprocess.TimeoutExpired):
        return False


def revoke_permissions() -> None:
    """Revoke cached sudo credentials."""
    try:
        subprocess.run(['sudo', '--remove-timestamp'], check=False)
    except Exception:  # pylint: disable=broad-exception-caught
        # Don't raise. App is shutting down.
        pass
