# 패키지 불러오기
import pymysql
import pandas as pd
import yahoo_fin.stock_info as si
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
query_fs = """
    insert into global_fs (account, date, value, freq, ticker)
    values (%s,%s,%s,%s,%s) as new
    on duplicate key update
    value = new.value;
"""


# 오류 발생시 저장할 리스트 생성
error_list = []

# fs_empty = pd.DataFrame({'account' : [None],                                                  
#                          'date' : [None],
#                          'value' : [None],
#                          'freq' : [None],     
#                          'ticker' : [None]                                               
#                          })


# 전종목 주가 다운로드 및 저장
for i in tqdm(range(0, len(ticker_list))): 

    # 빈 데이터프레임 복사
    # data_fs = fs_empty.copy()  
    
    # 티커 선택
    ticker = ticker_list['Symbol'][i]        
    
    # 오류 발생 시 이를 무시하고 다음 루프로 진행
    try:
        
       # 재무제표 다운로드
       data_y = si.get_financials(ticker, yearly=True, quarterly=False)
       data_fs_y = pd.concat([v for k, v in data_y.items()])
       data_fs_y = data_fs_y.stack().reset_index()
       data_fs_y.columns = ['account', 'date', 'value']
       data_fs_y['freq'] = 'y'

       data_q = si.get_financials('AAPL', yearly=False, quarterly=True)
       data_fs_q = pd.concat([v for k, v in data_q.items()])
       data_fs_q = data_fs_q.stack().reset_index()
       data_fs_q.columns = ['account', 'date', 'value']
       data_fs_q['freq'] = 'q'
       
       data_fs = pd.concat([data_fs_y, data_fs_q], axis = 0)
       data_fs['ticker'] = ticker       
       
       # 주가 데이터를 DB에 저장
       args  = data_fs.values.tolist() 
       mycursor.executemany(query_fs, args)
       con.commit()
    
    except:
        
        # 오류 발생시 빈 데이터프레임을 불러온 후 다음 루프로 이동                
        error_list.append(ticker)      
    
    # 타임슬립 적용
    time.sleep(2)    
    
# DB 연결 종료
con.close()    