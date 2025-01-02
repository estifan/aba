def has_fractional_seconds(datetime_string):
    # Split by the space to separate date and time
    try:
        time_part = datetime_string.split(" ")[-1]
        # Check if the seconds part contains a decimal
        return "." in time_part.split(":")[-1]
    except IndexError:
        return False  # Handle invalid formats gracefully