"""Authenticate for sudo commands."""
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
            show="*",
            parent=parent
        )
        if not _password:
            parent.quit_app("Cancelled.")

        try:
            subprocess.run(['sudo', '-S', '-v'],
                           input=_password + '\n',
                           text=True,
                           capture_output=True,
                           timeout=20,  # Unlikely, but better than hanging.
                           check=True)

            _password = None  # Overwrite immediately.
            return
        except subprocess.CalledProcessError as exc:
            if attempt < max_tries - 1:
                stderr = exc.stderr or ""
                if 'try again' in stderr.lower():
                    messagebox.showerror("Error", "Incorrect password.",
                                         parent=parent)
                else:
                    # Fallback for any other sudo validation error.
                    messagebox.showerror(
                        "Error",
                        f"Authentication failed:\n{stderr.strip() or exc}",
                        parent=parent,
                    )

        except Exception as exc:  # pylint: disable=broad-exception-caught
            # Defensively catch any unexpected errors and quit.
            parent.quit_on_error(f"Unexpected Error {exc}")

        finally:
            _password = None  # Ensure always cleared.

    # Failed every attempt.
    message = f"Authentication failed {max_tries} times.\n\nClick OK to Quit."
    parent.quit_on_error(message)
