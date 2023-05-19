import pandas as pd
import datetime
from random import randint

startDt = datetime.datetime.now().replace(hour=9,minute=10,second=0,microsecond=0)
endDt =  datetime.datetime.now().replace(hour=15,minute=0,second=0,microsecond=0)

time_list = pd.date_range(startDt, endDt, periods = 10)
time_list

time_list = time_list.round(freq = 's').tolist()
time_list

for i in range(10) :  
    print(randint(-10,10))
    
[i + datetime.timedelta(seconds = randint(-10,10)) for i in time_list]

