import sys
from datetime import datetime, timedelta

def parse_moment(line: str) -> datetime:
    # Мысал line: "2025-01-01 UTC+03:00"
    line = line.strip()
    date_part, tz_part = line.split()          # "2025-01-01", "UTC+03:00"

    y, m, d = map(int, date_part.split('-'))

    # tz_part: "UTC+03:00" немесе "UTC-05:30"
    sign = 1
    if tz_part[3] == '-':
        sign = -1

    hh = int(tz_part[4:6])
    mm = int(tz_part[7:9])

    offset = timedelta(hours=hh, minutes=mm) * sign

    local_midnight = datetime(y, m, d, 0, 0, 0)

    # UTC = local - offset
    return local_midnight - offset

def main():
    text = sys.stdin.buffer.read().decode("utf-8-sig")
    lines = [ln for ln in text.splitlines() if ln.strip() != ""]
    t1 = parse_moment(lines[0])
    t2 = parse_moment(lines[1])

    diff_seconds = abs((t1 - t2).total_seconds())
    days = int(diff_seconds // 86400)

    print(days)

if __name__ == "__main__":
    main()