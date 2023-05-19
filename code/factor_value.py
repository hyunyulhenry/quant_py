import pymysql
import pandas as pd
import numpy as np

con = pymysql.connect(
    user='root',passwd='1234', host='127.0.0.1', db='stock_db', charset='utf8'
)

ticker_list = pd.read_sql(
"""
select * from kor_ticker
where 기준일 = (select max(기준일) from kor_ticker) 
	and 종목구분 = '보통주';
""", con = con)

value_list = pd.read_sql(
"""
select * from kor_value
where 기준일 = (select max(기준일) from kor_value);
""", con = con)

con.close()

value_list.loc[value_list['값'] < 0, '값'] = np.nan
value_pivot = value_list.pivot(index = '종목코드', columns = '지표', values = '값')
data_bind = ticker_list[['종목코드', '종목명']].merge(value_pivot, how = 'left', on = '종목코드')

# PER, PBR 기준
value_rank = data_bind[['PER', 'PBR']].rank(axis = 0)
value_sum = value_rank.sum(axis = 1, skipna = False).rank()
data_bind.loc[value_sum <= 20, ['종목코드', '종목명', 'PER', 'PBR']]

# 상관관계
import matplotlib.pyplot as plt
import seaborn as sns

value_list_copy = data_bind.copy()
value_list_copy['DY'] = 1/value_list_copy['DY']
value_list_copy = value_list_copy[['PER', 'PBR', 'PCR', 'PSR', "DY"]]
value_rank_all = value_list_copy.rank(axis = 0)
mask = np.triu(value_rank_all.corr())

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(value_rank_all.corr(), annot = True, mask = mask, annot_kws = {"size" : 16},
            vmin=0, vmax=1, center= 0.5, cmap= 'coolwarm', square = True)
ax.invert_yaxis()

# 모든 지표 기준
value_sum_all = value_rank_all.sum(axis = 1, skipna = False).rank()
data_bind.loc[value_sum_all <= 20]

