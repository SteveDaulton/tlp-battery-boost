"""Tkinter UI and delegating."""
import subprocess
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import NoReturn

from battery_boost.authenticate import authenticate
from battery_boost.constants import (
    ThemeKeys,
    DEFAULT_THEME,
    BatteryState,
    STATES,
    REFRESH_INTERVAL_MS
)
from battery_boost.helper_functions import (
    check_tlp_installed
)
from battery_boost.tlp_command import (
    initialise_tlp,
    tlp_toggle_state, tlp_get_stats,
)
from battery_boost.tlp_parser import parse_tlp_stats


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
        if not check_tlp_installed():
            self.quit_on_error("TLP not found")

        # Acquire root for commands.
        self._refresh_job: str | None = None
        authenticate(self)

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
        initialise_tlp(self)
        self.write_stats(STATES[BatteryState.DEFAULT]['action'])
        self.apply_state()
        self.refresh_authentication()

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
        tlp_toggle_state(self, self.ui_state)
        # Flip UI state
        self.ui_state = (BatteryState.DEFAULT
                         if self.ui_state == BatteryState.RECHARGE
                         else BatteryState.RECHARGE)
        self.apply_state()

    def write_stats(self, action: str = "") -> None:
        """Update the text area with the current TLP battery stats."""
        raw_stats = tlp_get_stats()
        stats = f"{action}{parse_tlp_stats(raw_stats)}"
        print(stats)  # echo to terminal
        # noinspection PyTypeChecker
        self.text_box.config(state=tk.NORMAL)
        self.text_box.delete('1.0', tk.END)
        self.text_box.insert(tk.END, stats)
        # noinspection PyTypeChecker
        self.text_box.config(state=tk.DISABLED)
