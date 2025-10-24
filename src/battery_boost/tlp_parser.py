"""Parsing utilities for interpreting `tlp-stat -b` output."""

from collections import defaultdict


UNKNOWN = "???"


def parse_tlp_stats(tlp_stats: str) -> str:
    """Return formatted TLP battery stats or an error message.

    Parse the output of tlp_get_stats() into a readable
    format showing charge thresholds and capacities.

    Returns:
        str: Human-readable summary of battery stats or an error message.
    """
    if tlp_stats.lower().startswith('error'):
        return tlp_stats

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

    # Add the last battery
    if current_battery and battery_info:
        stats.append(_format_battery_str(current_battery, battery_info))

    return '\n'.join(stats) if stats else "No battery data found."


def _format_battery_str(name: str, info: defaultdict[str, str]) -> str:
    """Return parsed battery data as a human-readable block of text."""
    return (f"{name}:\n"
            f"  Start threshold: {info['start']}%\n"
            f"  End threshold: {info['end']}%\n"
            f"  Current Charge: {info['charge']}% "
            f"of {info['capacity']}%\n")


def _get_battery_value(line_text: str) -> str:
    """Return numeric value from a 'key = value' line, or ??? if missing."""
    parts = line_text.split('=', 1)
    if len(parts) != 2:
        return UNKNOWN
    value = parts[1].strip().split()[0]
    return value
