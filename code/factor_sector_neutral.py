import pymysql
import pandas as pd
from scipy.stats import zscore

con = pymysql.connect(
    user='root',passwd='1234', host='127.0.0.1', db='stock_db', charset='utf8'
)


ticker_list = pd.read_sql(
"""
select * from kor_ticker
where 기준일 = (select max(기준일) from kor_ticker) 
	and 종목구분 = '보통주';
""", con = con)

sector_list = pd.read_sql(
"""
select * from kor_sector
where 기준일 = (select max(기준일) from kor_ticker) ;	
""", con = con)

price_list = pd.read_sql(
"""
select 날짜, 종가, 종목코드
from kor_price
where 날짜 >= (select (select max(날짜) from kor_price) - interval 1 year);
""", con = con)

con.close()

price_pivot = price_list.pivot(index = '날짜', columns = '종목코드', values = '종가')
ret_list = pd.DataFrame(data = (price_pivot.iloc[-1] / price_pivot.iloc[0]) - 1, columns = ['return'])

# 합치기
data_bind = ticker_list[['종목코드', '종목명']].merge(sector_list[['CMP_CD', 'SEC_NM_KOR']],
                                   how = 'left', left_on = '종목코드', right_on = 'CMP_CD').\
    merge(ret_list, how = 'left', on = '종목코드')
    
# 단순 모멘텀 전략
import matplotlib.pyplot as plt

data_bind['rank'] = data_bind['return'].rank(axis = 0, ascending = False)
sector_count = pd.DataFrame(data_bind.loc[data_bind['rank'] <= 20, 'SEC_NM_KOR'].value_counts())
plt.rc('font', family = 'Malgun Gothic')
sector_count.plot.barh(figsize = (10, 6), legend = False)
plt.gca().invert_yaxis()

for y, x in enumerate(sector_count['SEC_NM_KOR']):
    plt.annotate(str(x), xy=(x, y), va='center')
    
    
# 섹터 중립화    
data_bind.loc[data_bind['SEC_NM_KOR'].isnull(), 'SEC_NM_KOR'] = '기타'
data_bind['z-score'] = data_bind.groupby('SEC_NM_KOR', dropna=False)['return'].apply(zscore, nan_policy='omit')
data_bind['z-rank'] = data_bind['z-score'].rank(axis = 0, ascending = False)
sector_neutral_count = pd.DataFrame(data_bind.loc[data_bind['z-rank'] <= 20, 'SEC_NM_KOR'].value_counts())

plt.rc('font', family = 'Malgun Gothic')
sector_neutral_count.plot.barh(figsize = (10, 6), legend = False)
plt.gca().invert_yaxis()

for y, x in enumerate(sector_neutral_count['SEC_NM_KOR']):
    plt.annotate(str(x), xy=(x, y), va='center')