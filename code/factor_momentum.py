import pymysql
import pandas as pd

con = pymysql.connect(
    user='root',passwd='1234', host='127.0.0.1', db='stock_db', charset='utf8'
)


ticker_list = pd.read_sql(
"""
select * from kor_ticker
where 기준일 = (select max(기준일) from kor_ticker) 
	and 종목구분 = '보통주';
""", con = con)


price_list = pd.read_sql(
"""
select 날짜, 종가, 종목코드
from kor_price
where 날짜 >= (select (select max(날짜) from kor_price) - interval 1 year);
""", con = con)

con.close()

# 피벗
price_pivot = price_list.pivot(index = '날짜', columns = '종목코드', values = '종가')

# 12개월 수익률 구하고 합치기
ret_list = pd.DataFrame(data = (price_pivot.iloc[-1] / price_pivot.iloc[0]) - 1, columns = ['return'])
data_bind = ticker_list[['종목코드', '종목명']].merge(ret_list, how = 'left', on = '종목코드')
    
# 단순 모멘텀 전략
momentum_rank = data_bind['return'].rank(axis = 0, ascending = False)
data_bind[momentum_rank <= 20]

# 시각화
price_momentum = price_list[price_list['종목코드'].isin(data_bind.loc[momentum_rank <= 20, '종목코드'])]

import seaborn as sns
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')
g = sns.FacetGrid(price_momentum, col = '종목코드', col_wrap = 5, sharey=False)
g = g.map(plt.plot, "날짜", "종가")
g.set(xticklabels=[])  
g.set(xlabel=None)
g.set(ylabel=None)


#------------------------#
# K Ratio ################

import statsmodels.api as sm
import numpy as np

ret = price_pivot.pct_change().iloc[1: ]
ret_cum = np.log(1+ret).cumsum()

x = np.array(range(len(ret)))
y = ret_cum.iloc[:, 0].values

reg = sm.OLS(y, x).fit()
reg.summary()

print(reg.params, reg.bse, (reg.params / reg.bse))

x = np.array(range(len(ret)))
k_ratio = {}
    
for i in range(0, len(ticker_list)) :    
    
    ticker = data_bind.loc[i, '종목코드']    
    
    try:
        y = ret_cum.loc[:, price_pivot.columns == ticker]
        reg = sm.OLS(y, x).fit()
        res = float(reg.params / reg.bse)
    except:
        res = np.nan
        
    k_ratio[ticker] = res

k_ratio_bind = pd.DataFrame.from_dict(k_ratio, orient = 'index').reset_index()
k_ratio_bind.columns = ['종목코드', 'K_ratio']


# K_ratio
data_bind = data_bind.merge(k_ratio_bind, how = 'left', on = '종목코드')
k_ratio_rank = data_bind['K_ratio'].rank(axis = 0, ascending = False)
data_bind[k_ratio_rank <= 20]

# 시각화
k_ratio_momentum = price_list[price_list['종목코드'].isin(data_bind.loc[k_ratio_rank <= 20, '종목코드'])]

plt.rc('font', family='Malgun Gothic')
g = sns.FacetGrid(k_ratio_momentum, col = '종목코드', col_wrap = 5, sharey=False)
g = g.map(plt.plot, "날짜", "종가")
g.set(xticklabels=[])  
g.set(xlabel=None)
g.set(ylabel=None)
