from datetime import datetime, timedelta

# Get current date and time
now = datetime.now()
print("Now:", now)

after_5_days = now + timedelta(days=5)
print("Date after 5 days:", after_5_days.date())

#3) Get yesterday by subtracting 1 day
yesterdaydate = now + timedelta(days = -1)
print("Yesterday:", yesterdaydate)

#Print only today's date (without time)
print("Today's date:", now.date())

#get tommorow by adding 1 day to current date
tommorowday = now + timedelta(days=1)
print("Tommorow:", tommorowday)

#Format date and time into a custom string: DD-MM-YYYY HH:MM:SS
formatted = now.strftime("%d-%m-%Y %H:%M:%S")
print("Formatted date/time:", formatted)