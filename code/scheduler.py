# https://pypi.org/project/schedule/
# https://schedule.readthedocs.io/en/stable/index.html

# https://blog.daum.net/geoscience/1626

import schedule
import time
import datetime

def job():
    print(datetime.datetime.now().strftime('%H:%M:%S'))    
    print("=====================")

schedule.every(3).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
    

# 현재 작업중인 리스트확인
schedule.get_jobs()
    
# Clear
schedule.clear_job(job) # 특정
schedule.clear() # 전부


# 시분할 
import pandas as pd
from datetime import timedelta
import schedule

startDt = datetime.datetime.now() + timedelta(seconds=3)
endDt =  datetime.datetime.now() + timedelta(seconds=20)

time_list = pd.date_range(startDt, endDt, periods = 10)
time_list = time_list.round(freq = 's').tolist()

time_list_sec = [i.strftime('%H:%M:%S') for i in time_list]

for i in time_list_sec:
    schedule.every().day.at(i).do(job)


while True:
    schedule.run_pending()
    
    if datetime.datetime.now() > endDt :
        print('End')
        break