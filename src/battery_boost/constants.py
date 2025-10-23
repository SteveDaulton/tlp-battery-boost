"""Battery Boost Constants."""
from enum import Enum
from typing import TypedDict


# 10 min interval between re-validating sudo password
REFRESH_INTERVAL_MS = 600_000


# UI Themes

class ThemeName(Enum):
    """Available themes."""
    LIGHT = 'light'
    DARK = 'dark'


ThemeKeys = TypedDict('ThemeKeys', {'background': str,
                                    'active': str,
                                    'text': str,
                                    'button_0': str,
                                    'active_0': str,
                                    'button_1': str,
                                    'active_1': str})


THEME: dict[ThemeName, ThemeKeys] = {
    ThemeName.LIGHT: {'background': 'white',
                      'active': 'gold',
                      'text': 'black',
                      'button_0': 'gainsboro',
                      'active_0': 'darkgray',
                      'button_1': 'goldenrod',
                      'active_1': 'darkgoldenrod'},
    ThemeName.DARK: {'background': 'gray15',
                     'active': 'firebrick4',
                     'text': 'white',
                     'button_0': 'gray30',
                     'active_0': 'gray40',
                     'button_1': 'firebrick',
                     'active_1': 'firebrick3'}
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
    """TLP states."""
    DEFAULT = 'default'
    RECHARGE = 'recharge'


UIState = TypedDict('UIState', {'action': str,
                                'label_text': str,
                                'button_text': str})


STATES: dict[BatteryState, UIState] = {
    BatteryState.DEFAULT: {
        'action': "TLP reset to current defaults.\n\n",
        'label_text': "Default TLP profile",
        'button_text': "Click to Recharge"
        },
    BatteryState.RECHARGE: {
        'action': "Charging to full capacity.\n\n",
        'label_text': "Full Recharge Enabled",
        'button_text': "Switch to Default"
        }
    }
