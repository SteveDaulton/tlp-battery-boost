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


ThemeKeys = TypedDict('ThemeKeys', {'background': str,
                                    'active': str,
                                    'text': str,
                                    'btn_normal': str,
                                    'btn_active_normal': str,
                                    'btn_charge': str,
                                    'btn_active_charge': str})


THEME: dict[ThemeName, ThemeKeys] = {
    ThemeName.LIGHT: {'background': 'white',
                      'active': 'gold',
                      'text': 'black',
                      'btn_normal': 'gainsboro',
                      'btn_active_normal': 'darkgray',
                      'btn_charge': 'goldenrod',
                      'btn_active_charge': 'darkgoldenrod'},
    ThemeName.DARK: {'background': 'gray15',
                     'active': 'firebrick4',
                     'text': 'white',
                     'btn_normal': 'gray30',
                     'btn_active_normal': 'gray40',
                     'btn_charge': 'firebrick',
                     'btn_active_charge': 'firebrick3'}
    }


DEFAULT_THEME = THEME[ThemeName.LIGHT]


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
