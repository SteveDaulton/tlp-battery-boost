# Battery Boost

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/SteveDaulton/tlp-battery-boost/blob/main/LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/tlp-battery-boost.svg)](https://pypi.org/project/tlp-battery-boost/)

<p align="center">
  <img src="https://raw.githubusercontent.com/SteveDaulton/tlp-battery-boost/main/BatteryBoost.png" alt="Battery Boost Screenshot">
</p>

_A lightweight Tkinter GUI to toggle TLP between normal battery optimization mode and temporary full-charge mode ( tlp fullcharge )._

## Overview

Battery Boost provides an easy-to-use interface for switching between normal and full-charge battery profiles using [TLP](https://linrunner.de/tlp/). It's designed for users who want to extend their battery lifespan by maintaining optimal charge levels during normal use, while having quick access to full charging when needed.

## Features

- Toggle Between Profiles: Switch between default TLP settings and full-charge mode
- Automatic Authentication: Enter your password once - the app maintains sudo privileges while running
- Battery Status Display: View current charge levels and threshold settings
- Theme Support: Choose between light and dark themes
- Adjustable Font Sizes: Scale the interface to your preference
- Terminal Integration: When run from terminal, displays status information for debugging

## Requirements

- Linux with TLP installed and configured
- Python 3.10+
- Tkinter (python3-tk)
- sudo privileges for TLP commands

## Installation

**Ensure TLP and Tkinter are installed on your system:**

```bash
sudo apt install tlp tlp-rdw python3-tk  # For Debian/Ubuntu
# or
sudo dnf install tlp tlp-rdw python3-tkinter  # For Fedora
```

**Installing with pipx (Recommended)**

```bash
pipx install tlp-battery-boost
```

**Optional Desktop Integration**

If you’d like Battery Boost to appear in your system’s application menu or on your desktop:

- Most Linux desktop environments (such as GNOME, KDE, XFCE) allow you to **add a custom launcher** manually.
- Set the command to `battery_boost` and (optionally) include options such as `battery_boost -t dark -f 2`.


## Usage

To launch the graphical interface:

```bash
battery_boost
```

The app will:

- Prompt for your sudo password
- Initialize TLP to default settings
- Show the current battery status
- Provide a button to toggle between default and full-charge modes


## Command Line Options

You can view the full command-line options by running:

```bash
battery_boost --help
```

Example output:

```text
battery_boost --help
usage: battery_boost [-h] [-v] [-f {1-5}] [-t {light,dark}]

A simple GUI to enable `tlp fullcharge`.

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -f {1-5}, --font-size {1-5}
                        Font size [1-5] (1=smallest, 5=largest) (default: 3)
  -t {light,dark}, --theme {light,dark}
                        Color theme (default: light)
```

**Notes:**

- `-f` sets the font size (1=smallest, 5=largest; default=3).  
- `-t` sets the color theme (light or dark; default=light).  
- `-v` prints the program version.  
- `-h` shows this help message and exits.


### Examples

**Large font with dark theme**

```
battery_boost -f 5 -t dark
```
 
**Small font for compact displays**

```
battery_boost --font-size 1
```

## How It Works

- Default Mode: Uses TLP's standard battery preservation settings (typically 80% charge limit)
- Full Charge Mode: Temporarily disables charge limits to charge the battery to 100%
- Authentication: Caches sudo credentials for 10 minutes to avoid repeated password prompts
- Status Monitoring: Uses `tlp-stat -b` to display current battery thresholds and charge levels

> For more information about TLP, see [https://linrunner.de/tlp/](https://linrunner.de/tlp/).


## Security Notes

- Your password is only used for initial sudo authentication and is immediately cleared from memory
- Your password is never written to disk.
- The sudo session is cleared and privileges are revoked on exit.
- No network connections are made - everything runs locally

## Troubleshooting

**Tkinter not available / ImportError: No module named 'tkinter':**

- Make sure Tkinter is installed (see the Installation section above).  
- On Linux, this usually requires the system package `python3-tk` (Debian/Ubuntu) or `python3-tkinter` (Fedora).

**TLP not found error:**

- Ensure TLP is installed and in your PATH
- Verify TLP is properly configured for your system

**Authentication issues:**

- Make sure you have sudo privileges
- Check that your password is correct

**Battery status not showing:**

- Verify your system's battery is detected by TLP
- Check that `sudo tlp-stat -b` works from the command line

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

Licensed under the [GNU General Public License v3.0](https://github.com/SteveDaulton/tlp-battery-boost/blob/main/LICENSE).

**Note:** This application requires TLP to be properly configured for your specific hardware.
Some battery conservation features may not be available on all systems.
