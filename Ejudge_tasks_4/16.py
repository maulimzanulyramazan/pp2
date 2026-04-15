from datetime import datetime, timedelta

def to_utc(line: str) -> datetime:
    # line: "YYYY-MM-DD HH:MM:SS UTC±HH:MM"
    date_str, time_str, tz_str = line.strip().split()

    # Parse local datetime (timezone info not applied yet)
    local_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")

    # tz_str example: "UTC+03:00" or "UTC-02:30"
    sign = 1 if tz_str[3] == '+' else -1
    hh = int(tz_str[4:6])
    mm = int(tz_str[7:9])

    offset_seconds = sign * (hh * 3600 + mm * 60)

    # UTC = local - offset
    return local_dt - timedelta(seconds=offset_seconds)

start_line = input().strip()
end_line = input().strip()

start_utc = to_utc(start_line)
end_utc = to_utc(end_line)

duration = int((end_utc - start_utc).total_seconds())
print(duration)