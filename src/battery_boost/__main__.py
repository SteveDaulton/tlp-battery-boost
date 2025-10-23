#!/usr/bin/env python3
"""
Battery Manager GUI using TLP.

Allows toggling between normal and full-charge battery profiles,
refreshing sudo authentication periodically to avoid repeated prompts.
"""

import argparse
import importlib.metadata
import shutil
import subprocess
import sys
import tkinter as tk

from collections import defaultdict
from tkinter import ttk
from tkinter import simpledialog, messagebox
from typing import Callable, NoReturn, TypeAlias

from battery_boost.constants import (REFRESH_INTERVAL_MS,
                                     THEME,
                                     ThemeName,
                                     ThemeKeys,
                                     DEFAULT_THEME,
                                     FONT_SIZES,
                                     BatteryState,
                                     STATES)


class App(tk.Tk):  # pylint: disable=too-many-instance-attributes
    """Tkinter GUI for controlling laptop battery charge behavior via TLP.

    The app toggles between normal ('default') and full-charge ('recharge')
    profiles, refreshing `sudo` authentication periodically so the user
    does not need to re-enter their password during normal use.
    """
    def __init__(self,
                 theme: ThemeKeys = DEFAULT_THEME,
                 standard_font: tuple[str, int] = ('TkDefaultFont', 12),
                 small_font: tuple[str, int] = ('TkDefaultFont', 9),
                 scale_factor: float = 1.0,
                 ) -> None:
        """Initialize UI, state, and TLP baseline configuration."""
        super().__init__()

        self.theme = theme
        self.standard_font = standard_font
        self.small_font = small_font
        self.scale_factor = scale_factor

        self.withdraw()
        self.protocol('WM_DELETE_WINDOW', self.quit_app)

        # Fail early if TLP not available.
        if not self.check_tlp_installed():
            self.quit_on_error("TLP not found")

        # Acquire root for commands.
        self._refresh_job: str | None = None
        self.authenticate()

        self.ui_state: BatteryState = BatteryState.DEFAULT

        self.title('Battery Boost')
        self.geometry(f'{int(400 * self.scale_factor)}x{int(360 * self.scale_factor)}')
        self.minsize(int(200 * self.scale_factor), int(150 * self.scale_factor))
        self.maxsize(int(600 * self.scale_factor), int(600 * self.scale_factor))

        # ttk Style setup
        self.style = ttk.Style(self)
        self.style.theme_use('clam')  # 'clam' allows color customizations.

        # Create styles for both states
        self.style.configure('Default.TButton',
                             relief='flat',
                             background=self.theme['button_0'],
                             foreground=self.theme['text'],
                             font=self.standard_font)
        self.style.map('Default.TButton',
                       background=[('active', self.theme['active_0'])])

        self.style.configure('Recharge.TButton',
                             relief='flat',
                             background=self.theme['button_1'],
                             foreground=self.theme['text'],
                             font=self.standard_font)
        self.style.map('Recharge.TButton',
                       background=[('active', self.theme['active_1'])])

        self.style.configure('Default.TLabel',
                             background=self.theme['background'],
                             foreground=self.theme['text'],
                             font=self.standard_font)
        self.style.configure('Recharge.TLabel',
                             background=self.theme['active'],
                             foreground=self.theme['text'],
                             font=self.standard_font)

        # Widgets

        self.label = ttk.Label(self,
                               style='Default.TLabel',
                               border=int(10 * self.scale_factor))
        self.label.pack()

        self.button = ttk.Button(self,
                                 style='Default.TButton',
                                 command=self.toggle_state)
        self.button.pack()

        instructions = ("You can close this app after\n"
                        "selecting the required profile.")
        self.instruction_label = ttk.Label(self,
                                           style='Default.TLabel',
                                           text=instructions,
                                           justify='center',
                                           font=self.small_font)
        self.instruction_label.pack(pady=(int(5 * self.scale_factor),
                                          int(10 * self.scale_factor)))

        self.text_box = tk.Text(self, height=2,
                                bg=self.theme['background'],
                                foreground=self.theme['text'],
                                font=self.small_font)
        # noinspection PyTypeChecker
        self.text_box.pack(padx=int(10 * self.scale_factor),
                           pady=int(10 * self.scale_factor),
                           expand=True,
                           fill=tk.BOTH)
        # noinspection PyTypeChecker
        self.text_box.config(state=tk.DISABLED)

        # Show main window.
        self.deiconify()

        # Ensure TLP is in a known (default enabled) state.
        self.initialise_tlp()
        self.write_stats(STATES[BatteryState.DEFAULT]['action'])
        self.apply_state()
        self.refresh_authentication()

    @staticmethod
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

    def authenticate(self) -> None:
        """Prompt user for sudo password and validate.

        Runs `sudo -v` to cache credentials for subsequent commands.
        Retries up to three times before exiting the program.

        Exits program if authentication fails.
        """
        max_tries = 3
        for attempt in range(max_tries):
            password = simpledialog.askstring(
                "Authenticate",
                "Authentication Required to run Battery Boost.\n\nEnter your password:",
                show="*",
                parent=self
                )
            if not password:
                self.quit_app("Cancelled.")

            try:
                subprocess.run(['sudo', '-S', '-v'],
                               input=password + '\n',
                               text=True,
                               capture_output=True,
                               check=True)
                # noinspection PyUnusedLocal
                password = None  # Overwrite immediately.
                return

            except subprocess.CalledProcessError as exc:
                if attempt < max_tries - 1:
                    stderr = exc.stderr or ""
                    if 'try again' in stderr.lower():
                        messagebox.showerror("Error", "Incorrect password.")
                    else:
                        # Fallback for any other sudo validation error.
                        messagebox.showerror(
                            "Error",
                            f"Authentication failed:\n{stderr.strip() or exc}",
                            parent=self,
                            )

            except Exception as exc:  # pylint: disable=broad-exception-caught
                # Defensively catch any unexpected errors and quit.
                self.quit_on_error(f"Unexpected Error {exc}")

            finally:
                # noinspection PyUnusedLocal
                password = None  # Ensure always cleared.

        # Failed every attempt.
        message = f"Authentication failed {max_tries} times.\n\nClick OK to Quit."
        self.quit_on_error(message)

    def initialise_tlp(self) -> None:
        """Initialize TLP to default state.

        Runs `sudo tlp start` to reset the TLP configuration before use.
        """
        try:
            subprocess.run(['sudo', 'tlp', 'start'], check=True)
            return

        except Exception as exc:  # pylint: disable=broad-exception-caught
            messagebox.showerror("Unexpected Error",
                                 f"Could not initialize TLP.\n{exc}",
                                 parent=self)
            self.quit_app(f"Error: Could not initialize TLP: {exc}")

    def refresh_authentication(self) -> None:
        """Refresh authentication.

        Validate sudo authentication periodically to keep it active
        while app is running.
        """
        try:
            subprocess.run(['sudo', '-v'], check=True)
        except (subprocess.CalledProcessError, OSError) as exc:
            self.quit_app(f"Authentication failure: {exc}")

        # noinspection PyTypeChecker
        self._refresh_job = self.after(REFRESH_INTERVAL_MS, self.refresh_authentication)

    def quit_on_error(self, error_message: str, title: str = "Error") -> NoReturn:
        """Display Error dialog and quit."""
        messagebox.showerror(title, error_message, parent=self)
        self.quit_app(f"Error: {error_message}")

    def quit_app(self, status: int | str = 0) -> NoReturn:
        """Terminate the application.

        Cancels any scheduled refresh jobs, destroys the Tk root window,
        and calls `sys.exit`.

        Args:
            status: Optional exit code or message.
        """
        if self._refresh_job:
            try:
                self.after_cancel(self._refresh_job)
            except (tk.TclError, RuntimeError) as exc:
                print(f"quit_app failed to cancel job {exc}")
        self.destroy()
        sys.exit(status)

    def apply_state(self) -> None:
        """Update widgets and text area to display the current UI state."""
        state = STATES[self.ui_state]

        # Colors:
        background = (self.theme['background']
                      if self.ui_state is BatteryState.DEFAULT
                      else self.theme['active'])

        text_color = self.theme['text']

        # Change window background
        self.configure(bg=background)

        # Update label text & style
        label_style = ('Recharge.TLabel'
                       if self.ui_state is BatteryState.RECHARGE
                       else 'Default.TLabel')
        self.label.configure(style=label_style,
                             text=state['label_text'],
                             background=background,
                             foreground=text_color)
        self.instruction_label.configure(style=label_style,
                                         background=background,
                                         foreground=text_color)

        # Update button text & style
        button_style = ('Recharge.TButton'
                        if self.ui_state is BatteryState.RECHARGE
                        else 'Default.TButton')
        self.button.configure(style=button_style, text=state['button_text'])

        # Text box
        self.text_box.config(bg=background, fg=text_color)
        self.write_stats(state['action'])

    def toggle_state(self) -> None:
        """Toggle between default and recharge profiles.

        Updates the UI and runs the corresponding TLP command.
        """
        # Flip state
        if self.ui_state == BatteryState.RECHARGE:
            self.ui_state = BatteryState.DEFAULT
            command = ['sudo', 'tlp', 'start']
        else:
            self.ui_state = BatteryState.RECHARGE
            command = ['sudo', 'tlp', 'fullcharge']

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as exc:
            self.quit_on_error(f"TLP command failed: {exc.returncode}:\n"
                               f"{exc.stderr or exc}")
        except FileNotFoundError as exc:
            self.quit_on_error(f"Command not found: {exc.filename}")
        except OSError as exc:
            self.quit_on_error(f"System error while running TLP command: {exc}")

        self.apply_state()

    def write_stats(self, action: str = "") -> None:
        """Update the text area with the current TLP battery stats."""
        stats = f"{action}{self.get_tlp_stats()}"
        print(stats)  # echo to terminal

        # noinspection PyTypeChecker
        self.text_box.config(state=tk.NORMAL)
        self.text_box.delete('1.0', tk.END)
        self.text_box.insert(tk.END, stats)
        # noinspection PyTypeChecker
        self.text_box.config(state=tk.DISABLED)

    def get_tlp_stats(self) -> str:
        """Return formatted TLP battery stats or an error message.

        Executes `sudo tlp-stat -b` and parses the output into a readable
        format showing charge thresholds and capacities.

        Returns:
            str: Human-readable summary of battery stats or an error message.
        """
        try:
            result = subprocess.run(['sudo', 'tlp-stat', '-b'],
                                    text=True,
                                    capture_output=True,
                                    check=True)
        except subprocess.CalledProcessError as exc:
            return f"Failed to run tlp-stat:\n{exc.stderr or exc}"
        except OSError as exc:
            return f"System error while running tlp-stat: {exc}"
        except Exception as exc:  # pylint: disable=broad-exception-caught
            return f"Unexpected error: {exc}"

        lines = result.stdout.splitlines()
        stats = []
        current_battery = ""
        battery_info: defaultdict[str, str] = defaultdict(lambda: "???")

        for line in lines:
            line = line.strip()
            # Detect start of a new battery section
            if line.startswith('+++ ') and 'Battery Status:' in line:
                # Save previous battery (if any)
                if current_battery:
                    stats.append(self.format_battery(current_battery, battery_info))

                # Start new one
                current_battery = line.split('Battery Status:')[1].strip()
                battery_info = defaultdict(lambda: "???")
                continue

            # Parse values.
            # Using Python string methods rather than regex for maintainability.
            get_value: Callable[[str], str] = (
                lambda full_line: full_line.split('=', 1)[1].strip().split()[0])

            if 'charge_control_start_threshold' in line:
                battery_info['start'] = get_value(line)
            elif 'charge_control_end_threshold' in line:
                battery_info['end'] = get_value(line)
            elif line.startswith('Charge'):
                battery_info['charge'] = get_value(line)
            elif line.startswith('Capacity'):
                battery_info['capacity'] = get_value(line)

        # Don’t forget the last battery
        if current_battery and battery_info:
            stats.append(self.format_battery(current_battery, battery_info))

        return '\n'.join(stats) if stats else "No battery data found."

    @staticmethod
    def format_battery(name: str, info: defaultdict[str, str]) -> str:
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
    finally:
        subprocess.run(['sudo', '-K'], check=False)


if __name__ == '__main__':
    main()
