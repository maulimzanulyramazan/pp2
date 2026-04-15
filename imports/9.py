from datetime import datetime
from zoneinfo import ZoneInfo
a = input()
b = input()
tz_ny = datetime.now(ZoneInfo(f"{a}/{b}"))
print(f"{a} {b}:", tz_ny.strftime("%d/%m/%y , %H:%M:%S"))