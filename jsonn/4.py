from datetime import datetime, timedelta
now = datetime.now()
nt = datetime(now.year + 1, 1, 1)
ny = nt - now
print(ny.days)