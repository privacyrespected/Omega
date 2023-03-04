import datetime
import holidays as hol





#new_york_tz = datetime.timezone(datetime.timedelta(hours=-5), name='America/New York')
new_york_tz = datetime.timezone(datetime.timedelta(hours=8), name='Asia/Hong_Kong')
now=datetime.datetime.now(new_york_tz)
openTime=datetime.time(hour=9,minute=30,second=0)
closeTime= datetime.time(hour=16,minute=0, second=0)
print(now)
today = datetime.datetime.today()
weekday = today.weekday()
print(now.time())
currenttime = now.time()
currenttime = int(currenttime)
if (now.time()<openTime) or (now.time()>closeTime):
    if weekday<6:
        status="OPEN" #true
        print(status)
else:
    status="CLOSE" #false
    print(status)


