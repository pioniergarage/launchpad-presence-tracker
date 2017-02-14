import re, datetime

from lib import Activity

# Pattern for MAC addresses.
# Example "B6:B7:E3:AC:D8:09"
MAC_PATTERN = r"(([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2}))"

# Pattern for not associated string.
# Example "(not associated) "
NOT_ASSOCIATED_PATTERN = r"(\(not associated\) )"

# Pattern for MAC addresses or not associated string.
# Examples: "B6:B7:E3:AC:D8:09" or "(not associated) "
MAC_OR_NOT_ASSOCIATED_PATTERN = r"({0}|{1})".format(MAC_PATTERN, NOT_ASSOCIATED_PATTERN)

# Pattern for datetime.
# Example: "2016-12-27 14:11:06"
DATETIME_PATTERN = r"([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})"

# Other pattern without "\n" or ","
# Examples: "      -42" or "UPC4514352"
OTHER_PATTERN = r"([^\n|,]*)"

# Pattern for a station line.
# Example: "B6:B7:E3:AC:D8:09, 2016-12-27 14:11:06, 2016-12-27 14:11:15,
#           -80,      3, (not associated) ,UPC4514352"
LINE_PATTERN = r"^{0}, {1}, {2},{3},{4}, {5},{6}".format(
    MAC_PATTERN,
    DATETIME_PATTERN,
    DATETIME_PATTERN,
    OTHER_PATTERN,
    OTHER_PATTERN,
    MAC_OR_NOT_ASSOCIATED_PATTERN,
    OTHER_PATTERN)

LINE_REGEX = re.compile(LINE_PATTERN)
NOT_ASSOCIATED_REGEX = re.compile(NOT_ASSOCIATED_PATTERN)

def extract_activities(lines):
    """
    Returns the activities extracted from data lines.

    Returns:
        activities (list): the extracted activities.
    """
    activities = []

    for line in lines:
        activity = extract_activity(line)
        if activity:
            activities.append(activity)

    activities.sort(key=lambda a: a.last)

    return activities

def extract_activity(line):
    """
    Returns the activity the line or None if no activity can be extracted.

    Returns:
        activity (Activity): the extracted activity.
    """
    match = LINE_REGEX.search(line)
    if match:
        mac_str = match.group(1)
        first_str = match.group(4)
        last_str = match.group(5)
        bssid_str = match.group(8)
        if NOT_ASSOCIATED_REGEX.match(bssid_str):
            bssid_str = None
        try:
            first_datetime = datetime.datetime.strptime(first_str, "%Y-%m-%d %H:%M:%S")
            last_datetime = datetime.datetime.strptime(last_str, "%Y-%m-%d %H:%M:%S")
            return Activity(mac_str, first_datetime, last_datetime, bssid_str)
        except ValueError:
            pass
    return None
