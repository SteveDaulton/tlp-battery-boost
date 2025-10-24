#!/usr/bin/env python3
"""Entry point for the Battery Boost application.

Initialises and launches the Tkinter GUI for managing TLP battery charge profiles.
Battery Boost allows users to toggle between normal optimization and full-charge modes,
with battery status display.
"""

import subprocess
import sys

from battery_boost.app import App
from battery_boost.helper_functions import parse_args


def main() -> None:
    """Configure and launch app."""
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
        print(f"Fatal error: {exc}", file=sys.stderr)
        sys.exit(1)
    finally:
        subprocess.run(['sudo', '-K'], check=False)


if __name__ == '__main__':
    main()
