# 상관관계 분석

import pymysql
import pandas as pd
import numpy as np

con = pymysql.connect(
    user='root',passwd='1234', host='127.0.0.1', db='stock_db', charset='utf8'
)

value_list = pd.read_sql(
"""
select * from kor_value
where 기준일 = (select max(기준일) from kor_value)
and 지표 = 'PBR';
""", con = con)

fs_list = pd.read_sql(
"""
select * from kor_fs
where 계정 in ('매출총이익', '자산')
and 공시구분 = 'y';
""", con = con)

con.close()

value_list.loc[value_list['값'] < 0, '값'] = np.nan
value_pivot = value_list.pivot(index = '종목코드', columns = '지표', values = '값')

fs_list = fs_list.sort_values(['종목코드', '계정', '기준일'])
fs_list = fs_list.groupby(['종목코드', '계정']).tail(1)
fs_list_pivot = fs_list.pivot(index = '종목코드', columns = '계정', values = '값')
fs_list_pivot['GPA'] = fs_list_pivot['매출총이익'] / fs_list_pivot['자산']

bind_rank = value_pivot['PBR'].rank().to_frame().merge(fs_list_pivot['GPA'].rank(ascending = False), how = 'inner', on = '종목코드')

bind_rank.corr()

# 시각화
import matplotlib.pyplot as plt

bind_data = value_list.merge(fs_list_pivot, how = 'left', on = '종목코드')
bind_data = bind_data.dropna()
bind_data['PBR_quantile'] = pd.qcut(bind_data['값'], q = 5, labels = range(1, 6))
bind_group = bind_data.groupby('PBR_quantile').mean('GPA')

fig, ax = plt.subplots(figsize=(10, 6))
plt.rc('font', family = 'Malgun Gothic')
plt.bar(x = np.arange(5), height = bind_group['GPA'])
plt.xlabel('PBR')
plt.ylabel('GPA')

plt.show()
