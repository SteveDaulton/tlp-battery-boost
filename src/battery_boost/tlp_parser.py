"""Parsing utilities for interpreting `tlp-stat -b` output."""

from collections import defaultdict


UNKNOWN = "???"


def parse_tlp_stats(tlp_stats: str) -> str:
    """Parse TLP battery stats and return a human-readable summary.

    Args:
        tlp_stats: Output string from `tlp_get_stats()`.

    Returns:
        str: Formatted battery statistics or an error message.
    """
    if not tlp_stats.strip():
        return "No battery data found."

    lines = tlp_stats.splitlines()
    stats = []
    current_battery = ""
    battery_info: defaultdict[str, str] = defaultdict(lambda: UNKNOWN)

    for line in lines:
        line = line.strip()
        # Detect start of a new battery section
        if line.startswith('+++ ') and 'Battery Status:' in line:
            # Save previous battery (if any)
            if current_battery:
                stats.append(_format_battery_str(current_battery, battery_info))

            # Start new one
            try:
                current_battery = line.split('Battery Status:')[1].strip()
            except IndexError:
                pass
            battery_info = defaultdict(lambda: UNKNOWN)
            continue

        # Parse values.
        if 'charge_control_start_threshold' in line:
            battery_info['start'] = _get_battery_value(line)
        elif 'charge_control_end_threshold' in line:
            battery_info['end'] = _get_battery_value(line)
        elif line.startswith('Charge'):
            battery_info['charge'] = _get_battery_value(line)
        elif line.startswith('Capacity'):
            battery_info['capacity'] = _get_battery_value(line)
        elif 'status' in line:
            battery_info['status'] = _get_battery_status(line)

    # Add the last battery
    if current_battery and battery_info:
        stats.append(_format_battery_str(current_battery, battery_info))

    return '\n'.join(stats) if stats else "No battery data found."


def _format_battery_str(battery_name: str, info: defaultdict[str, str]) -> str:
    """Format battery info into a readable text block.

    Args:
        battery_name: Battery name.
        info: Dictionary of battery attributes (start, end, charge, capacity).

    Returns:
        str: Formatted string representing the battery.
    """
    return (f"Current Status: {info['status']}\n\n"
            f"{battery_name}:\n"
            f"  Start threshold: {info['start']}%\n"
            f"  End threshold: {info['end']}%\n"
            f"  Current Charge: {info['charge']}% "
            f"of {info['capacity']}%\n"
            )


def _get_battery_value(line_text: str) -> str:
    """Extract the numeric battery value from a TLP output line.

    Args:
        line_text: A line from `tlp-stat -b` containing a battery property,
                   e.g. start/end thresholds, charge, or capacity.

    Returns:
        str: The numeric value as a string (e.g., '70', '83.8'), or '???' if not found.
    """
    parts = line_text.split('=', 1)
    if len(parts) != 2:
        return UNKNOWN
    token = parts[1].strip().split()[0]
    try:
        float(token)
    except ValueError:
        return UNKNOWN
    return token


def _get_battery_status(line_text: str) -> str:
    """Extract the battery status from a TLP output line."""
    parts = line_text.split('=')
    if len(parts) != 2:
        return UNKNOWN
    return parts[1].strip()
