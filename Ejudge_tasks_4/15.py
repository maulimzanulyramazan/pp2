import sys
from datetime import datetime, timedelta, date

def parse_line(line: str):
    # "2001-07-01 UTC+05:30"
    line = line.strip()
    date_part, tz_part = line.split()
    y, m, d = map(int, date_part.split('-'))

    sign = 1
    if tz_part[3] == '-':
        sign = -1
    hh = int(tz_part[4:6])
    mm = int(tz_part[7:9])
    offset = timedelta(hours=hh, minutes=mm) * sign

    return y, m, d, offset

def is_leap_year(y: int) -> bool:
    return (y % 400 == 0) or (y % 4 == 0 and y % 100 != 0)

def birthday_date_for_year(bm: int, bd: int, y: int) -> date:
    # Feb 29 rule
    if bm == 2 and bd == 29 and not is_leap_year(y):
        return date(y, 2, 28)
    return date(y, bm, bd)

def local_midnight_to_utc(d: date, offset: timedelta) -> datetime:
    # local midnight in its timezone -> UTC
    local = datetime(d.year, d.month, d.day, 0, 0, 0)
    return local - offset

def ceil_days(seconds: int) -> int:
    # seconds >= 0
    return (seconds + 86399) // 86400

def main():
    text = sys.stdin.buffer.read().decode("utf-8-sig")
    lines = [ln for ln in text.splitlines() if ln.strip()]

    by, bm, bd, birth_offset = parse_line(lines[0])
    cy, cm, cd, curr_offset = parse_line(lines[1])

    current_date = date(cy, cm, cd)
    current_utc = local_midnight_to_utc(current_date, curr_offset)

    # candidate birthday in current year (cy)
    cand_date = birthday_date_for_year(bm, bd, cy)
    cand_utc = local_midnight_to_utc(cand_date, birth_offset)

    # if candidate is earlier than current moment -> next year
    if cand_utc < current_utc:
        cand_date = birthday_date_for_year(bm, bd, cy + 1)
        cand_utc = local_midnight_to_utc(cand_date, birth_offset)

    delta = cand_utc - current_utc  # >= 0
    seconds = delta.days * 86400 + delta.seconds  # бүтін секунд

    # IMPORTANT: ceil days, not floor
    print(ceil_days(seconds))

if __name__ == "__main__":
    main()