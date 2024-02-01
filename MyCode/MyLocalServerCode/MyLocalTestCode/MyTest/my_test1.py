def time_to_seconds(time_str):
    parts = time_str.split(",")
    hours = 0
    minutes = 0
    seconds = 0

    for part in parts:
        if "hours" in part:
            hours = int(part.strip().split()[0])
        elif "minutes" in part:
            minutes = int(part.strip().split()[0])
        elif "seconds" in part:
            seconds = int(part.strip().split()[0])

    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

time_str1 = "4 hours, 56 minutes"
time_str2 = "56 minutes, 14 seconds"

seconds1 = time_to_seconds(time_str1)
seconds2 = time_to_seconds(time_str2)

print(seconds1)
print(seconds2)