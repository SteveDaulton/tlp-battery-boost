# Usage Guide

## Overview

**TLP Battery Boost** provides a simple graphical interface for adjusting TLP’s battery charge thresholds.  
It is intended for laptops that support charge-limit control via TLP.

---

## Launching the Application

After installation (via pipx or pip):

```
battery_boost
```

### Password Prompt

When launched, the application first requests your **sudo password**.  
This is required because TLP charge-control commands (e.g. `tlp fullcharge`) need root privileges.

The graphical interface appears **after** successful authentication.

If you cancel the password dialog, the application quits.

---

## Main Interface

When launched, the application displays:

- **Current TLP state** which is initially the default profile.
- **Current battery status** (charging, waiting to charge, or discharging).
- **Current battery thresholds** (Start charge and End charge thresholds).
- **Current battery charge** as a percentage.
- **Click to Recharge** button, to enable full charging.

### Colour Indicators

Battery Boost uses colour to indicate the current charging mode and power state:

- **Normal battery-care mode**
  - The main window uses the standard theme background  
    (white in the light theme, dark grey in the dark theme).
- **Full-Charge Boost enabled**
  - The main window turns green  
    (light green in the light theme, dark green in the dark theme).

**Button Colour:**

- In battery-care mode, the button appears neutral (for example, light grey in the
  light theme).
- When Full-Charge Boost is active, the button adopts a green shade to match the
  active charging mode.
- If **AC power is disconnected**, the button turns **red** to indicate that the
  battery is **discharging**.

**Note:**

If your laptop has more than one battery installed, you may need to resize
the interface to view the details in full.

---

## Usage

1. Ensure AC power is connected to the laptop
2. Launch the app
3. Enter your `sudo` password
4. Check the displayed charge level
5. Click the button to commence charging to full capacity

The application background will appear green when charging to full is enabled.

The application may now be closed. Charging to full will continue under TLP
control for as long as AC power remains connected.

Alternatively, you may keep **Battery Boost** open
to monitor the battery level in real time.

### Cancel full charging

Full charge mode may be cancelled by clicking the button again. This re-applies
the configured TLP battery-care thresholds.

Alternatively, if the TLP configuration option `RESTORE_THRESHOLDS_ON_BAT` is enabled,
configured thresholds are restored automatically when AC power is disconnected.
