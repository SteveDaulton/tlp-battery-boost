# Troubleshooting

This page covers the common errors and warnings that may be encountered when using
**TLP Battery Boost**, along with suggested actions.

---

## "Authentication failed 3 times."

**Cause:** The user did not enter the correct sudo password in three attempts.

**Action:**

- Ensure you are typing the correct sudo password.
- If you continue to have trouble, verify that your user can run `sudo` commands from the terminal.

---

## "Password required."

**Cause:** The user submitted an empty password in the authentication dialog.

**Action:** Enter your sudo password to proceed.

---

## "Incorrect password."

**Cause:** The user entered the wrong sudo password.

**Action:** Try again with the correct password. Maximum three attempts are allowed.

---

## "sudo not found on this system."

**Cause:** Either `sudo` is not installed, or it is not available in your PATH, or your user cannot run sudo.

**Action:**

- Install `sudo` using your distribution’s package manager, e.g.:
- Ensure your user is allowed to run `sudo`:
- If you see “user is not in the sudoers file”, add your user to the sudoers list following your distro’s documentation.

---

## "Authentication process timed out."

**Cause:** Sudo prompt took too long or hung.

**Action:** Retry launching the app.
Ensure your system is responsive and no other modal dialogs are blocking sudo prompts.

---

## "Unexpected Error ..." (during authentication)

**Cause:** Some unexpected error occurred when running sudo.

**Action:** Check that `sudo` is installed and operational. Launch a terminal and run:

```sh
sudo -v
```

Resolve any issues reported there before relaunching the app.

---

## TLP errors

These include:

- "TLP is not installed or not in PATH."
- "Error: Could not initialize TLP."
- "TLP command failed"
- "System error while running TLP command"
- "Command not found: ..."

**Cause:** The app cannot execute the necessary TLP commands. This can happen if TLP is
not installed correctly, if AC power is not connected (for `tlp fullcharge`), or due to system errors.

**Action:**

- Verify TLP is installed and operational by running in a terminal:

  ```
  tlp-stat -s
  sudo tlp fullcharge
  ```
- Ensure AC power is connected when using full-charge mode.
- If commands fail, resolve TLP issues before using Battery Boost.

---

## AC power required dialog
### "Full charge mode requires AC power..."

**Cause:** The app detects that your laptop is not plugged into AC power.

**Action:** Connect your laptop to AC power and try again. Click "Retry" in the dialog.

---

## "No battery data found."

**Cause:** TLP failed to provide battery statistics.

**Action:**

- Ensure TLP is installed and active.
- Run in terminal to verify:

```
sudo tlp-stat -b
```
- If the command returns battery data, relaunch the app. If not, investigate TLP configuration.

---

## Thresholds/charge appear as "???"

**Cause:** The battery information could not be read.

**Action:**

- Ensure TLP is installed and active.
- Ensure TLP is properly configured for your system.

---

**General Note:** If you see any other errors, ensure that TLP is correctly installed and
configured on your system as per the [installation guide](installation.md#installing-tlp-battery-boost).
