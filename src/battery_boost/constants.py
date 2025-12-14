"""Constants and types for the Battery Boost application."""

from enum import Enum
from typing import TypedDict


DEBUG = False
"""Enable debug logging (True/False)."""


REFRESH_INTERVAL_MS: int = 1_000
"""Check TLP battery statistics every second.
Must be frequent enough to catch changes in charging status.
"""


# UI Themes

class ThemeName(Enum):
    """Available themes.

    Currently available themes:
        - LIGHT: Light theme
        - DARK: Dark theme
    """
    LIGHT = 'light'
    DARK = 'dark'


class ThemeKeys(TypedDict):
    """Colours used in the GUI theme for Battery Boost.

    Attributes:
        default_bg: Background colour of the main window in normal mode.
        charge_bg: Background colour when full charge mode is active.
        text: Colour of standard text.
        btn_normal: Colour of the button in normal mode.
        btn_active_normal: Button colour when pressed in normal mode.
        btn_charge: Colour of the button in full-charge mode.
        btn_active_charge: Button colour when pressed in full-charge mode.
        btn_discharge: Colour of the button when battery is discharging.
        btn_active_discharge: Button colour when pressed while discharging.
        btn_discharge_text: Text colour for the button while discharging.
    """
    default_bg: str
    charge_bg: str
    text: str
    btn_normal: str
    btn_active_normal: str
    btn_charge: str
    btn_active_charge: str
    btn_discharge: str
    btn_active_discharge: str
    btn_discharge_text: str


THEME: dict[ThemeName, ThemeKeys]
"""Mapping of ThemeName to the corresponding colour scheme."""


_THEME: dict[ThemeName, ThemeKeys] = {
    ThemeName.LIGHT: {'default_bg': '#FFFFFF',
                      'charge_bg': '#BBFFBB',
                      'text': '#000000',
                      'btn_normal': '#DDDDDD',
                      'btn_active_normal': '#CCCCCC',
                      'btn_charge': '#99DD99',
                      'btn_active_charge': '#88EE88',
                      'btn_discharge': '#DD0000',
                      'btn_active_discharge': '#FF0000',
                      'btn_discharge_text': '#FFFFFF'},
    ThemeName.DARK: {'default_bg': '#222233',
                     'charge_bg': '#114411',
                     'text': '#FFFFFF',
                     'btn_normal': '#555555',
                     'btn_active_normal': '#666666',
                     'btn_charge': '#228822',
                     'btn_active_charge': '#009900',
                     'btn_discharge': '#DD0000',
                     'btn_active_discharge': '#FF0000',
                     'btn_discharge_text': '#FFFFFF'}
    }

# Public constant documented separately to avoid rendering large literals in API docs.
THEME = _THEME


DEFAULT_THEME = THEME[ThemeName.DARK]
"""Default theme."""


# Font Sizes

FontSizeConfig = tuple[tuple[str, int], tuple[str, int], float]
"""Font size configuration used by the GUI.

Contains:
    - (font name, size) for the standard UI font
    - (font name, size) for the small UI font
    - GUI scale factor
"""


FONT_SIZES: dict[int, FontSizeConfig]
"""Font configurations for the GUI.

    - Keys: size level (1–5)
    - Values: tuple of ((standard font, size), (small font, size), scale factor)"""


# (standard font, small font, GUI scale factor)
_FONT_SIZES = {1: (('TkDefaultFont', 8), ('TkDefaultFont', 7), 0.72),
               2: (('TkDefaultFont', 10), ('TkDefaultFont', 8), 0.84),
               3: (('TkDefaultFont', 12), ('TkDefaultFont', 10), 1.0),
               4: (('TkDefaultFont', 14), ('TkDefaultFont', 12), 1.2),
               5: (('TkDefaultFont', 18), ('TkDefaultFont', 14), 1.4)}

# Public constant documented separately to avoid rendering large literals in API docs.
FONT_SIZES = _FONT_SIZES


# State definitions

class BatteryState(Enum):
    """Battery profiles managed by TLP."""
    DEFAULT = 'default'
    RECHARGE = 'recharge'


class UIState(TypedDict):
    """Labels and actions for the battery state displayed in the GUI."""
    action: str
    label_text: str
    button_text: str


STATES: dict[BatteryState, UIState]
"""Mapping of battery state to UI labels and actions."""


_STATES: dict[BatteryState, UIState] = {
    BatteryState.DEFAULT: {
        'action': "TLP reset to current defaults.\n",
        'label_text': "Default TLP profile",
        'button_text': "Click to Recharge"
        },
    BatteryState.RECHARGE: {
        'action': "Charging to full capacity.\n",
        'label_text': "Full Recharge Enabled",
        'button_text': "Switch to Default"
        }
    }

# Public constant documented separately to avoid rendering large literals in API docs.
STATES = _STATES
