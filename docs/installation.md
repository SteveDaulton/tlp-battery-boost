# Installation

## Requirements

Before installing **TLP Battery Boost**, ensure the following prerequisites are met:

- A **Linux laptop** with an internal battery and AC power
- **TLP installed and configured**
- Hardware that supports [**TLP Battery Care**](https://linrunner.de/tlp/settings/bc-vendors.html).
- **Python 3.10+**
- **python3-tk** (Tkinter)


---

## Install TLP

TLP must be installed and active for this application to work.

Most Linux distributions provide TLP through their package manager, but installation steps vary.

To install the latest version of TLP, refer to the official TLP documentation:

[TLP installation guide](https://linrunner.de/tlp/installation/)


After installing TLP, ensure it is enabled and running:

```
sudo tlp start
```

Use the following command to check that TLP is enabled and active:

```
tlp-stat -s
```

---

## Install python3-tk (Tkinter)

On many Linux distributions, Tkinter is packaged separately from Python.  
Install it using your distribution’s package manager:

### Debian / Ubuntu / Mint
```
sudo apt install python3-tk
```

### Fedora-based Linux systems
```
sudo dnf install python3-tkinter
```

### Arch-based Linux systems
```
sudo pacman -S tk
```

### CentOS, RedHat, and Oracle Linux systems:

Package names on YUM-based distributions can vary.
If `python3-tkinter` is not available, run `sudo yum search tkinter` to locate the correct one.
```
sudo yum install python3-tkinter
```

---

## Installing TLP Battery Boost

### Recommended: Install via pipx (PyPI)

The preferred installation method is to use **pipx**, which keeps the application isolated
from system packages while still providing a command on your PATH.Install **pipx** using
your distribution’s package manager  

Then install TLP Battery Boost from PyPI:

```
pipx install tlp-battery-boost
```

Launch the application:

```
battery_boost
```

**Note:** Battery Boost will prompt for sudo password on launch. This is required
to run TLP commands.

---

### Alternative: Install from Source (GitHub)

1. Clone the repository:

    ```
    git clone https://github.com/SteveDaulton/tlp-battery-boost.git
    cd tlp-battery-boost
    ```

2. Create a virtual environment:

    ```
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install the package:

    ```
    pip install .
    ```

4. Run the application:

    ```
    battery_boost
    ```

---

### Optional: Create a Desktop Launcher

TLP Battery Boost includes a suitable icon (`tlp-battery-boost.png`) for use in desktop launchers.

If you would like the application to appear in your desktop environment’s application menu,
create a .desktop entry:

```
~/.local/share/applications/tlp-battery-boost.desktop
```

With contents such as:

```
[Desktop Entry]
Type=Application
Name=TLP Battery Boost
Exec=battery_boost
Icon=tlp-battery-boost
Terminal=false
Categories=Utility;
```

Make the launcher executable:

```
chmod +x ~/.local/share/applications/tlp-battery-boost.desktop
update-desktop-database ~/.local/share/applications
```

Most desktop environments will locate the icon automatically if it is placed in a standard user
icon directory (e.g., `~/.local/share/icons/`).

---

### Notes

- Installing via **pipx** is recommended for isolation and convenience.  
- Installing from source is useful for development or testing.

---

## Uninstallation

### If installed via pipx

```sh
pipx uninstall tlp-battery-boost
```

### If installed from source or with pip

Remove the virtual environment or uninstall using:

```sh
pip uninstall tlp-battery-boost
```

If running from a cloned repository, simply delete the directory.

---

## Next steps

Proceed to the **[Usage guide](usage.md)** to learn how to operate the application.
