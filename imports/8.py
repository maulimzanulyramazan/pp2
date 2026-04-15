from datetime import datetime
from zoneinfo import ZoneInfo
tz_ny = datetime.now(ZoneInfo('America/New_York'))
tz_tokyo = datetime.now(ZoneInfo('Asia/Tokyo'))
tz_london = datetime.now(ZoneInfo('Europe/London'))
print("New York:", tz_ny.strftime("%A/%h/%y , %H:%M:%S"))
print("Tokyo:", tz_tokyo.strftime("%A/%h/%y , %H:%M:%S"))
print("London:", tz_london.strftime("%A/%h/%y , %H:%M:%S"))
tz_almaty = datetime.now(ZoneInfo('Asia/Almaty'))
print("Almaty:", tz_almaty.strftime("%d/%m/%Y , %H:%M:%S"))