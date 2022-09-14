from datetime import datetime
from pytz import timezone
import pytz

def pst_time():
    date = datetime.now(tz=pytz.utc)
    date = date.astimezone(timezone('US/Pacific'))
    #print(date)
    return date

#pst_time()