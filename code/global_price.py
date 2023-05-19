# 패키지 불러오기

import pymysql
import pandas as pd
import pandas_datareader as web
import time
from tqdm import tqdm


# DB 연결
con = pymysql.connect(
    user='root', passwd='1234', host='127.0.0.1', db='stock_db', charset='utf8'
)

mycursor = con.cursor()

# 티커리스트 불러오기
ticker_list = pd.read_sql("""
select * from global_ticker
where date = (select max(date) from global_ticker)
and country = 'United States';
""", con = con)

# DB 저장 쿼리
query = """
    insert into global_price (Date, High, Low, Open, Close, Volume, `Adj Close`, ticker)
    values (%s, %s,%s,%s,%s,%s,%s,%s) as new
    on duplicate key update
    High = new.High, Low = new.Low, Open = new.Open, Close = new.Close,
    Volume = new.Volume, `Adj Close` = new.`Adj Close`;
"""

# 오류 발생시 저장할 리스트 생성
error_list = []

# price_empty = pd.DataFrame({'Date' : date.today().strftime("%Y-%m-%d"),
#                             'High' : [None],
#                             'Low' : [None],
#                             'Open' : [None],
#                             'Close' : [None],
#                             'Volumne' : [None],
#                             'Adj Close' : [None]
#                             })


# 전종목 주가 다운로드 및 저장
for i in tqdm(range(0, len(ticker_list))): 

    
    # 티커 선택
    ticker = ticker_list['Symbol'][i]    
    
    
    # 오류 발생 시 이를 무시하고 다음 루프로 진행
    try:
        
        # url 생성     
        price = web.DataReader(ticker, 'yahoo')
                
        # 데이터 클렌징
        price = price.reset_index()
        price['ticker'] = ticker
        
        # 주가 데이터를 DB에 저장
        args  = price.values.tolist()

        mycursor.executemany(query, args)
        con.commit()
    
    except:
        
        # 오류 발생시 error_list에 티커 저장하고 넘어가기
        print(ticker)
        error_list.append(ticker)    
       
    # 타임슬립 적용
    time.sleep(2)    
    
# DB 연결 종료
con.close()    