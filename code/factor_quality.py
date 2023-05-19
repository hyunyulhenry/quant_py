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
""",con = con)

fs_list = pd.read_sql(
"""
select * from kor_fs
where 계정 in ('지배주주순이익', '매출총이익', '영업활동으로인한현금흐름', '자산', '지배기업주주지분')
and 공시구분 = 'q';
""", con = con)

con.close()

# ttm 계산
fs_list = fs_list.sort_values(['종목코드', '계정', '기준일'])
fs_list['ttm'] = fs_list.groupby(['종목코드', '계정'], as_index=False)['값'].rolling(window = 4, min_periods = 4).sum()['값']
fs_list_clean = fs_list.copy()
fs_list_clean['ttm'] = np.where(fs_list_clean['계정'].isin(['자산', '지배기업주주지분']), fs_list_clean['ttm'] / 4, fs_list_clean['ttm'])

fs_list_clean = fs_list_clean.groupby(['종목코드', '계정']).tail(1)

fs_list_pivot = fs_list_clean.pivot(index = '종목코드', columns = '계정', values = 'ttm')
fs_list_pivot['ROE'] = fs_list_pivot['지배주주순이익'] / fs_list_pivot['지배기업주주지분']
fs_list_pivot['GPA'] = fs_list_pivot['매출총이익'] / fs_list_pivot['자산']
fs_list_pivot['CFO'] = fs_list_pivot['영업활동으로인한현금흐름'] / fs_list_pivot['자산']

quality_list = ticker_list[['종목코드', '종목명']].merge(fs_list_pivot, how = 'left', on = '종목코드')

# 랭킹 구하기
quality_list_copy = quality_list[['ROE', 'GPA', 'CFO']].copy()
quality_rank = quality_list_copy.rank(ascending = False, axis = 0)


# 상관관계
import matplotlib.pyplot as plt
import seaborn as sns

mask = np.triu(quality_rank.corr())
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(quality_rank.corr(), annot = True, mask = mask, annot_kws = {"size" : 16},
            vmin=0, vmax=1, center= 0.5, cmap= 'coolwarm', square = True)
ax.invert_yaxis()
plt.show()


# 종목 선택
quality_sum = quality_rank.sum(axis = 1, skipna = False).rank()
quality_list.loc[quality_sum <= 20, ['종목코드', '종목명', 'ROE', 'GPA', 'CFO']].round(4)

