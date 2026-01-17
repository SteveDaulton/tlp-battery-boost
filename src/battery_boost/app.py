"""Tkinter GUI for managing TLP battery charge profiles.

Provides a simple interface to toggle between normal and full-charge modes,
refresh sudo authentication, and display battery statistics.
"""
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
    command_on_path,
    get_battery_stats,
    on_ac_power
)
from battery_boost.shell_commands import (
    initialise_tlp,
    tlp_toggle_state,
    tlp_active,
    tlp_running
)


class App(tk.Tk):  # pylint: disable=too-many-instance-attributes
    """Tkinter GUI for toggling TLP battery charge profiles.

    Supports switching between normal ('default') and full-charge ('recharge') modes
    and periodically refreshes display of battery statistics.
    """
    def __init__(self,
                 theme: ThemeKeys = DEFAULT_THEME,
                 standard_font: tuple[str, int] = ('TkDefaultFont', 12),
                 small_font: tuple[str, int] = ('TkDefaultFont', 10),
                 scale_factor: float = 1.0,
                 ) -> None:
        """Initialize the Tkinter UI, state, and baseline TLP configuration.

        Args:
            theme: Theme colors to apply.
            standard_font: Font for main UI elements.
            small_font: Font for secondary UI elements.
            scale_factor: Scale factor for UI sizing.
        """
        super().__init__()
        self._refresh_job: str | None = None

        self.theme = theme
        self.standard_font = standard_font
        self.small_font = small_font
        self.scale_factor = scale_factor
        self.withdraw()
        self.protocol('WM_DELETE_WINDOW', self.quit_app)

        # Fail early if TLP not available.
        self._verify_tlp_ready()

        while not self.ensure_ac_power():
            # Keep checking until either we have AC power, or we exit.
            pass

        # Acquire root for commands.
        authenticate(self)

        self.ui_state: BatteryState = BatteryState.DEFAULT

        self._init_window()
        self._init_styles()
        self._init_widgets()
        self._layout_widgets()

        # Bind Ctrl+Q keyboard shortcut
        self.bind('<Control-KeyPress-q>', lambda e: self.quit_app())

        # Show main window.
        self.deiconify()

        # Ensure TLP is in a known (default enabled) state.
        initialise_tlp(self)
        self.apply_state()
        self.battery_stats = get_battery_stats()
        self.write_stats(self.battery_stats['info'])
        self.refresh_battery_stats()

    def _init_window(self) -> None:
        """Initialize the window."""
        self.title('Battery Boost')
        self.geometry(f'{int(400 * self.scale_factor)}x{int(450 * self.scale_factor)}')
        self.minsize(int(200 * self.scale_factor), int(150 * self.scale_factor))
        self.maxsize(int(600 * self.scale_factor), int(600 * self.scale_factor))

    def _init_styles(self) -> None:
        """ttk Style setup"""
        style = ttk.Style(self)
        style.theme_use('clam')  # 'clam' allows color customizations.

        # Button state styles.
        btn_common = {'relief': 'flat', 'font': self.standard_font}

        _opts = {**btn_common,
                 'background': self.theme['btn_normal'],
                 'foreground': self.theme['text']}
        style.configure('Default.TButton', **_opts)
        style.map('Default.TButton',
                  background=[('active', self.theme['btn_active_normal'])])

        _opts = {**btn_common,
                 'background': self.theme['btn_charge'],
                 'foreground': self.theme['text']}
        style.configure('Recharge.TButton', **_opts)
        style.map('Recharge.TButton',
                  background=[('active', self.theme['btn_active_charge'])])

        _opts = {**btn_common,
                 'foreground': self.theme['btn_discharge_text'],
                 'background': self.theme['btn_discharge']}
        style.configure('Discharge.TButton', **_opts)
        style.map('Discharge.TButton',
                  background=[('active', self.theme['btn_active_discharge'])])

        # Label styles - Top Label.
        top_label_common = {'foreground': self.theme['text'],
                            'font': self.standard_font}
        _opts = {**top_label_common, 'background': self.theme['default_bg']}
        style.configure('Default.TLabel', **_opts)

        _opts = {**top_label_common, 'background': self.theme['charge_bg']}
        style.configure('Recharge.TLabel', **_opts)

        # Instruction label.
        instruction_label_common = {'foreground': self.theme['text'],
                                    'font': self.small_font}
        _opts = {**instruction_label_common, 'background': self.theme['default_bg']}
        style.configure('DefaultInstruction.TLabel', **_opts)

        _opts = {**instruction_label_common, 'background': self.theme['charge_bg']}
        style.configure('RechargeInstruction.TLabel', **_opts)

        self.style = style

    def _init_widgets(self) -> None:
        self.top_label = ttk.Label(self, style='Default.TLabel')
        self.button = ttk.Button(self,
                                 style='Default.TButton',
                                 command=self.toggle_state)
        instructions = ("AC power must be connected.\n\n"
                        "You can close this app after\n"
                        "selecting the required profile.")
        self.instruction_label = ttk.Label(self,
                                           style='DefaultInstruction.TLabel',
                                           text=instructions,
                                           justify='center')
        self.text_box = tk.Text(self, height=2,
                                background=self.theme['default_bg'],
                                foreground=self.theme['text'],
                                font=self.small_font)
        # noinspection PyTypeChecker
        self.text_box.config(state=tk.DISABLED)

    def _layout_widgets(self) -> None:
        self.top_label.pack(pady=int(10 * self.scale_factor))
        self.button.pack()
        self.instruction_label.pack(pady=(int(5 * self.scale_factor),
                                          int(10 * self.scale_factor)))
        # noinspection PyTypeChecker
        self.text_box.pack(padx=int(10 * self.scale_factor),
                           pady=int(10 * self.scale_factor),
                           expand=True,
                           fill=tk.BOTH)

    def _verify_tlp_ready(self) -> None:
        """Verify that TLP is installed and active. Quit on fatal error."""
        if not command_on_path('tlp'):
            self.quit_on_error("TLP is not installed or not in PATH.",
                               "Fatal Error")
        if command_on_path('systemctl'):
            if not tlp_running():
                self.quit_on_error("TLP service is not active.",
                                   "Fatal Error")
        elif not tlp_active():  # Less reliable fallback.
            self.quit_on_error("TLP service is not active.",
                               "Fatal Error")

    def ensure_ac_power(self) -> bool:
        """Check if api is on AC power.

        Returns:
        True if AC power is confirmed, else False.
        """
        try:
            if on_ac_power():
                return True
        except RuntimeError as exc:
            self.quit_on_error(str(exc), "Unsupported system")
        retry = messagebox.askretrycancel(
            "AC Power Required",
            "Full charge mode requires AC power.\n"
            "Plug in your laptop and try again.",
            parent=self,
            icon='warning'
        )
        if not retry:  # Cancel button pressed.
            self.quit_app("AC power not connected.")
        return False  # Non-fatal failure

    def refresh_battery_stats(self) -> None:
        """Periodically refresh the battery statistics."""
        new_battery_stats = get_battery_stats()
        current_battery_info = self.battery_stats['info']
        new_battery_info = new_battery_stats['info']
        # Handle updating button appearance on battery discharge.
        self.update_button(new_battery_stats['discharging'])
        # Update text widget info.
        if current_battery_info != new_battery_info:
            self.battery_stats = new_battery_stats
            self.write_stats(new_battery_info)

        # noinspection PyTypeChecker
        self._refresh_job = self.after(REFRESH_INTERVAL_MS, self.refresh_battery_stats)

    def update_button(self, is_discharging: bool) -> None:
        """Update button appearance to match battery status."""
        prev_btn_style = self.button.cget("style")
        if is_discharging:
            new_style = 'Discharge.TButton'
        elif self.ui_state is BatteryState.RECHARGE:
            new_style = 'Recharge.TButton'
        else:
            new_style = 'Default.TButton'
        if new_style != prev_btn_style:
            self.button.configure(style=new_style)

    def quit_on_error(self, error_message: str, title: str = "Error") -> NoReturn:
        """Display Error dialog and quit."""
        messagebox.showerror(title, error_message, parent=self)
        self.quit_app(f"Error: {error_message}")

    def quit_app(self, status: int | str = 0) -> NoReturn:
        """Terminate the application, cancel scheduled jobs, and exit.

        Args:
            status: Optional exit code or message.
        """
        if self._refresh_job:
            try:
                self.after_cancel(self._refresh_job)
            except (tk.TclError, RuntimeError):
                pass  # Just quit
        self.destroy()
        sys.exit(status)

    def apply_state(self) -> None:
        """Update the UI to reflect the current battery profile state."""
        state = STATES[self.ui_state]

        # Window background (non-style background change)
        background = (self.theme['default_bg']
                      if self.ui_state is BatteryState.DEFAULT
                      else self.theme['charge_bg'])
        self.configure(background=background)

        # Update styles
        if self.ui_state is BatteryState.RECHARGE:
            top_label_style = 'Recharge.TLabel'
            instruction_label_style = 'RechargeInstruction.TLabel'
            button_style = 'Recharge.TButton'
        else:
            top_label_style = 'Default.TLabel'
            instruction_label_style = 'DefaultInstruction.TLabel'
            button_style = 'Default.TButton'

        self.top_label.configure(style=top_label_style, text=state['label_text'])
        self.instruction_label.configure(style=instruction_label_style)
        self.button.configure(style=button_style, text=state['button_text'])

        # Text box (tk widget does not have ttk style).
        self.text_box.config(background=background, foreground=self.theme['text'])

    def toggle_state(self) -> None:
        """Switch between default and full-charge profiles and update the UI."""
        if not tlp_toggle_state(self, self.ui_state):
            return
        # Flip UI state
        self.ui_state = (BatteryState.DEFAULT
                         if self.ui_state == BatteryState.RECHARGE
                         else BatteryState.RECHARGE)
        self.apply_state()

        # Update text widget.
        self.battery_stats = get_battery_stats()
        self.write_stats(self.battery_stats['info'])
        return

    def write_stats(self, stats: str) -> None:
        """Update the text area with the current TLP battery stats."""
        stats = STATES[self.ui_state]['action'] + stats
        # noinspection PyTypeChecker
        self.text_box.config(state=tk.NORMAL)
        self.text_box.delete('1.0', tk.END)
        self.text_box.insert(tk.END, stats)
        # noinspection PyTypeChecker
        self.text_box.config(state=tk.DISABLED)
