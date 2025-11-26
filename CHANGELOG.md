# Changelog

All notable changes to **Battery Boost** are documented in this file.

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and [Semantic Versioning](https://semver.org/).


## 1.1.0 — 2025-11-29

### Added

- `CHANGELOG.md` added.
- Automatic debug-level logging for detailed diagnostic output.
- New `on_ac_power()` helper for a more direct and reliable AC-power check.
- Warning when fullcharge is requested on battery power.
- Button now turns **red** when the battery is discharging.
- Example `.desktop` launcher added to the documentation.


### Changed

- Substantial refactor for clarity, robustness, and consistent error handling.
    Includes major improvements to widget styling, attribute consistency,
    and theme handling.
- Improved TLP validation and readiness checks.
- Updated theme colours.
- Improved handling of “no AC power”, with clearer user feedback.
- README updates: consistent English spelling and updated screenshot.


### Fixed

- Periodic battery-status refresh (Fixes **#1**). 
    Battery stats now refresh **once per second** for live monitoring.
    (In 1.0.0 stats updated only when switching profiles.)
- Treat attempting `tlp fullcharge` while on battery power as non-fatal (Fixes **#2**).  
    The user may now attach AC and retry without the application exiting.
- Default font sizes updated to align with `FONT_SIZES[3]`.


## 1.0.0 — 2025-10-25

### Summary

First stable release of **Battery Boost**, providing a lightweight graphical interface for managing TLP battery-charging modes.

### Added

- **Tkinter GUI application** for toggling between TLP’s normal battery-optimised mode and full-charge mode (`tlp fullcharge`).
- **Battery status display** using `tlp-stat -b`, showing charge levels and threshold information.
- **Authentication system** with:
    - Single sudo prompt on startup
    - Cached credentials via sudo timeout
    - Privilege revocation on exit
- **Theme support:** Light and dark themes.
- **Adjustable font sizes:** Five user-selectable sizes, including CLI options.
- **Command-line integration:**  
    `--font-size`, `--theme`, `--version`, plus debug output when run from a terminal.
- **TLP readiness checks** and parsing of TLP output for battery values.
- **Documentation:** Comprehensive README including installation, usage, screenshots, security notes, and troubleshooting.

### Fixed

- Corrected invalid classifier in `pyproject.toml`.
