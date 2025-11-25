"""Constants and types for the Battery Boost application."""

from enum import Enum
from typing import TypedDict


DEBUG = False


# Check TLP battery statistics every second.
# Must be frequent enough to catch changes in charging status.
REFRESH_INTERVAL_MS: int = 1_000


# UI Themes

class ThemeName(Enum):
    """Available themes."""
    LIGHT = 'light'
    DARK = 'dark'


ThemeKeys = TypedDict('ThemeKeys', {'default_bg': str,
                                    'charge_bg': str,
                                    'text': str,
                                    'btn_normal': str,
                                    'btn_active_normal': str,
                                    'btn_charge': str,
                                    'btn_active_charge': str,
                                    'btn_discharge': str,
                                    'btn_active_discharge': str,
                                    'btn_discharge_text': str
                                    })


THEME: dict[ThemeName, ThemeKeys] = {
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


DEFAULT_THEME = THEME[ThemeName.DARK]


# Font Sizes

# (standard font, small font, GUI scale factor)
FONT_SIZES = {1: (('TkDefaultFont', 8), ('TkDefaultFont', 7), 0.72),
              2: (('TkDefaultFont', 10), ('TkDefaultFont', 8), 0.84),
              3: (('TkDefaultFont', 12), ('TkDefaultFont', 10), 1.0),
              4: (('TkDefaultFont', 14), ('TkDefaultFont', 12), 1.2),
              5: (('TkDefaultFont', 18), ('TkDefaultFont', 14), 1.4)}


# State definitions

class BatteryState(Enum):
    """Battery profiles managed by TLP."""
    DEFAULT = 'default'
    RECHARGE = 'recharge'


UIState = TypedDict('UIState', {'action': str,
                                'label_text': str,
                                'button_text': str})


STATES: dict[BatteryState, UIState] = {
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
