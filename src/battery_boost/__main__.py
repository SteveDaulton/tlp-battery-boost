#!/usr/bin/env python3
"""Entry point for the Battery Boost application.

Initialises and launches the Tkinter GUI for managing TLP battery charge profiles.
Battery Boost allows users to toggle between normal optimization and full-charge modes,
with battery status display.
"""
import logging
import sys

from battery_boost.app import App
from battery_boost.constants import DEBUG
from battery_boost.helper_functions import parse_args
from battery_boost.shell_commands import revoke_permissions


def main() -> None:
    """Entry point of the TLP Battery Boost application.

    - Configures the logging level based on the `DEBUG` constant.
    - Parses command-line arguments to determine the GUI theme and font settings.
    - Instantiates the main `App` class with the chosen theme and fonts.
    - Starts the Tkinter main event loop.
    - Handles user interrupts and ensures clean shutdown.
    - Revokes any elevated permissions acquired during execution.

    Exceptions:
        KeyboardInterrupt: Gracefully exits if the user sends an interrupt
            signal (e.g., Ctrl+C). The GUI is destroyed if it was created.
        Exception: Any unhandled exception during app initialization or
            execution is logged as critical and causes the program to exit
            with a non-zero status.
    """
    debug_level = logging.DEBUG if DEBUG else logging.WARNING
    logging.basicConfig(
        level=debug_level,
        format="%(levelname)s: %(name)s %(message)s",
    )

    theme_choice, font_normal, font_small, factor = parse_args(sys.argv[1:])
    app = None
    try:
        app = App(theme_choice, font_normal, font_small, factor)
        app.mainloop()
    except KeyboardInterrupt:
        if app:
            app.destroy()
    # Catchall if App fails to launch with unhandled exception.
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logging.critical(exc)
        sys.exit(1)
    finally:
        revoke_permissions()


if __name__ == '__main__':
    main()
