from datetime import datetime, time
import datetime
start_time=time(9,30,0)
end_time= time(16,0,0)
new_york_tz = datetime.timezone(datetime.timedelta(hours=8), name='Asia/Hong_Kong')
now=datetime.datetime.now(new_york_tz).time()
if start_time <= now <= end_time:
    print("The current time is within the time range.")
else:
    print("The current time is outside the time range.")

def marketstatus1():
    hong_kong_tz = datetime.timezone(datetime.timedelta(hours=8), name='Asia/Hong_Kong')
    now=datetime.datetime.now(hong_kong_tz)
    openTime=datetime.time(hour=9,minute=30,second=0)
    closeTime= datetime.time(hour=16,minute=0, second=0)
    today = datetime.datetime.today()
    weekday = today.weekday()
    if (now.time()<openTime) or (now.time()>closeTime):
        if weekday<6:
                    status = "OPEN"
                    return status
        else:
            status="CLOSED"
            return status
    else:
        status="CLOSED"
        return status