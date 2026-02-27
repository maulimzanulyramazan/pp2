from datetime import datetime, timedelta
# Get current date and time
now = datetime.now()
print("Now:", now)
after_5_days = now + timedelta(days=5)
print("Date after 5 days:", after_5_days.date())
yesterdaydate = now + timedelta(days = -1)
print("Yesterday:", yesterdaydate)
# Get only the date part
print("Today's date:", now.date())
# Add 7 days to the current date
tommorowday = now + timedelta(days=1)
print("Tommorow:", tommorowday)
# Format date and time as a string
formatted = now.strftime("%d-%m-%Y %H:%M:%S")
print("Formatted date/time:", formatted)