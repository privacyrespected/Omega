import datetime

# Get current time in Hong Kong
hong_kong_tz = datetime.timezone(datetime.timedelta(hours=8), name='Asia/Hong_Kong')
hong_kong_time = datetime.datetime.now(hong_kong_tz)

print("Hong Kong time:", hong_kong_time)


import datetime

# Get current time in New York
new_york_tz = datetime.timezone(datetime.timedelta(hours=-5), name='America/New_York')
new_york_time = datetime.datetime.now(new_york_tz)

print("New York time:", new_york_time)
import datetime

# Get the current time in a specific time zone
tz = datetime.timezone(datetime.timedelta(hours=8))  # Example: GMT+8
now = datetime.datetime.now(tz)
now=now.time()
now=now.strftime("%H:%M:%S")
# Print the time
print(now)

import holidays as hols
new_york_tz = datetime.timezone(datetime.timedelta(hours=-5), name='America/New_York')
us_holidays=hols.US()
now=datetime.datetime.now(new_york_tz)
openTime=datetime.time(hour=9,minute=30,second=0)
closeTime= datetime.time(hour=16,minute=0, second=0)
if now.date() in us_holidays:
    if (now.time()<openTime) or (now.time()>closeTime):
        if now.date().weekday>4:
            status="OPEN" #true
            print(status)
else:
    status="CLOSE" #false
    print(status)
