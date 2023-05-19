import pymysql
import pandas as pd
import numpy as np

con = pymysql.connect(
    user='root',passwd='1234', host='127.0.0.1', db='stock_db', charset='utf8'
)
query = """
select * from kor_ticker
where 기준일 = (select max(기준일) from kor_ticker) 
	and 종목구분 = '보통주';
"""
ticker_list = pd.read_sql(query,con = con)

fs_list = pd.read_sql(
"""
select * from kor_fs
where 계정 in ('매출액', '지배주주순이익', '법인세비용', '이자비용', '현금및현금성자산', '부채', '유동부채', '유동자산', '비유동자산', '감가상각비')
and 공시구분 = 'q';
""", con = con)

con.close()

fs_list = fs_list.sort_values(['종목코드', '계정', '기준일'])
fs_list['ttm'] = fs_list.groupby(['종목코드', '계정'], as_index=False)['값'].rolling(window = 4, min_periods = 4).sum()['값']
fs_list_clean = fs_list.copy()
fs_list_clean['ttm'] = np.where(fs_list_clean['계정'].isin(['부채', '유동부채', '유동자산', '비유동자산']), fs_list_clean['ttm'] / 4, fs_list_clean['ttm'])

fs_list_clean = fs_list_clean.groupby(['종목코드', '계정']).tail(1)
fs_list_pivot = fs_list_clean.pivot(index = '종목코드', columns = '계정', values = 'ttm')

data_bind = ticker_list[['종목코드', '종목명', '시가총액']].merge(fs_list_pivot, how = 'left', on = '종목코드')
data_bind['시가총액'] = data_bind['시가총액']  / 100000000

# 이익수익률 계산

## 분자(EBIT)
magic_ebit = data_bind['지배주주순이익'] + data_bind['법인세비용'] + data_bind['이자비용']

## 분모
magic_cap = data_bind['시가총액']
magic_debt = data_bind['부채']

magic_excess_cash = data_bind['유동부채'] - data_bind['유동자산'] + data_bind['현금및현금성자산']
magic_excess_cash[magic_excess_cash<0] = 0
magic_excess_cash_final = data_bind['현금및현금성자산'] - magic_excess_cash
magic_ev = magic_cap + magic_debt - magic_excess_cash_final

## 이익수익률
magic_ey = magic_ebit / magic_ev

# 투하자본 수익률
magic_ic = (data_bind['유동자산'] - data_bind['유동부채']) + (data_bind['비유동자산'] - data_bind['감가상각비'])
magic_roc = magic_ebit / magic_ic

# 열 입력하기
data_bind['이익 수익률'] = magic_ey
data_bind['투하자본 수익률'] = magic_roc

# 랭킹 구하기
magic_rank = (magic_ey.rank(ascending = False, axis = 0) + magic_roc.rank(ascending = False, axis = 0)).rank(axis = 0)
data_bind.loc[magic_rank <= 20, ['종목코드', '종목명', '이익 수익률', '투하자본 수익률']].round(4)

# 시각화
import matplotlib.pyplot as plt
import seaborn as sns

data_bind['투자구분'] = np.where(magic_rank <= 20, '마법공식', '기타')
sns.scatterplot(data = data_bind, x = '이익 수익률', y = '투하자본 수익률', hue = '투자구분', style = '투자구분')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.show()