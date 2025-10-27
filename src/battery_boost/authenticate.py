"""Prompt for and validate sudo credentials for Battery Boost.

Provides a GUI dialog to request the user's password and cache sudo credentials
for subsequent TLP commands. Exits the program if authentication fails.
"""

from __future__ import annotations
import subprocess
from tkinter import simpledialog, messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from battery_boost.app import App


def authenticate(parent: App) -> None:
    """Prompt user for sudo password and validate.

    Runs `sudo -v` to cache credentials for subsequent commands.
    Retries up to three times before exiting the program.

    Exits program if authentication fails.
    """
    max_tries = 3
    for attempt in range(max_tries):
        _password = simpledialog.askstring(
            "Authenticate",
            "Authentication Required to run Battery Boost.\n\nEnter your password:",
            show="*"
        )

        if _password is None:
            parent.quit_app("Cancelled.")

        # Don't strip() - whitespaces are unusual but valid password characters.
        if not _password:
            if attempt < max_tries - 1:
                messagebox.showerror("Error", "Password required.")
                continue
            else:
                break

        try:
            subprocess.run(['sudo', '-S', '-v'],
                           input=_password + '\n',
                           text=True,
                           capture_output=True,
                           timeout=20,  # Unlikely, but better than hanging.
                           check=True)
            _password = None  # Overwrite password immediately.
            return
        except FileNotFoundError:
            parent.quit_on_error("sudo not found on this system.")
        except subprocess.TimeoutExpired:
            parent.quit_on_error("Authentication process timed out.",
                                 "Fatal Error")
        except subprocess.CalledProcessError:
            # Only realistic failure remaining is "wrong password".
            if attempt < max_tries - 1:
                messagebox.showerror("Error", "Incorrect password.")
        except Exception as exc:  # pylint: disable=broad-exception-caught
            # Defensively catch any unexpected errors and quit.
            parent.quit_on_error(f"Unexpected Error {exc}")

        finally:
            _password = None  # Ensure always cleared.

    # Failed every attempt.
    message = f"Authentication failed {max_tries} times.\n\nClick OK to Quit."
    parent.quit_on_error(message)
