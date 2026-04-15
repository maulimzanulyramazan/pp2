from datetime import datetime
import pytz

local = datetime.now()
print("Local:", local.strftime("%m/%d/%Y, %H:%M:%S"))

tz_Tokyo = pytz.timezone('Asia/Tokyo')
datetime_Tokyo = datetime.now(tz_Tokyo)
print("Tokyo:", datetime_Tokyo.strftime("%m/%d/%Y, %H:%M:%S"))