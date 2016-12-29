import re, datetime

# Pattern for MAC addresses.
# Example "B6:B7:E3:AC:D8:09"
mac_pattern = r"(([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2}))"

# Pattern for not associated string.
# Example "(not associated) "
not_associated_pattern = r"(\(not associated\) )"

# Pattern for MAC addresses or not associated string.
# Examples: "B6:B7:E3:AC:D8:09" or "(not associated) "
mac_or_not_associated_pattern = r"({0}|{1})".format(mac_pattern, not_associated_pattern)

# Pattern for datetime.
# Example: "2016-12-27 14:11:06"
datetime_pattern = r"([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})"

# Other pattern without "\n" or ","
# Examples: "      -42" or "UPC4514352"
other_pattern = r"([^\n|,]*)"

# Pattern for a station line.
# Example: "B6:B7:E3:AC:D8:09, 2016-12-27 14:11:06, 2016-12-27 14:11:15, -80,      3, (not associated) ,UPC4514352"
line_pattern = r"^{0}, {1}, {2},{3},{4}, {5},{6}".format(
    mac_pattern,
    datetime_pattern,
    datetime_pattern,
    other_pattern,
    other_pattern,
    mac_or_not_associated_pattern,
    other_pattern)

line_regex = re.compile(line_pattern)
not_associated_regex = re.compile(not_associated_pattern)

def extract_activities(lines):
    activities = []

    for line in lines:
        activity = extract_activity(line)
        if activity:
            activities.append(activity)

    activities.sort(key=lambda a: a.last)

    return activities

def extract_activity(line):
    match = line_regex.search(line)
    if match:
        mac_str = match.group(1)
        first_str = match.group(4)
        last_str = match.group(5)
        bssid_str = match.group(8)
        if not_associated_regex.match(bssid_str):
            bssid_str = None
        try:
            first_datetime = datetime.datetime.strptime(first_str, "%Y-%m-%d %H:%M:%S")
            last_datetime = datetime.datetime.strptime(last_str, "%Y-%m-%d %H:%M:%S")
            return Activity(mac_str, first_datetime, last_datetime, bssid_str)
        except ValueError:
            return
