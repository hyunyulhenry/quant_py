import pymysql
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.stats import zscore
import matplotlib.pyplot as plt

con = pymysql.connect(
    user='root',passwd='1234', host='127.0.0.1', db='stock_db', charset='utf8'
)

ticker_list = pd.read_sql(
"""
select * from kor_ticker
where 기준일 = (select max(기준일) from kor_ticker) 
	and 종목구분 = '보통주';
""", con = con)

fs_list = pd.read_sql(
"""
select * from kor_fs
where 계정 in ('지배주주순이익', '매출총이익', '영업활동으로인한현금흐름', '자산', '지배기업주주지분')
and 공시구분 = 'q';
""", con = con)

value_list = pd.read_sql(
"""
select * from kor_value
where 기준일 = (select max(기준일) from kor_value);
""", con = con)

price_list = pd.read_sql(
"""
select 날짜, 종가, 종목코드
from kor_price
where 날짜 >= (select (select max(날짜) from kor_price) - interval 1 year);
""", con = con)

sector_list = pd.read_sql(
"""
select * from kor_sector
where 기준일 = (select max(기준일) from kor_ticker);	
""", con = con)

con.close()


# 데이터 핸들

## 퀄리티
fs_list = fs_list.sort_values(['종목코드', '계정', '기준일'])
fs_list['ttm'] = fs_list.groupby(['종목코드', '계정'], as_index=False)['값'].rolling(
    window=4, min_periods=4).sum()['값']
fs_list_clean = fs_list.copy()
fs_list_clean['ttm'] = np.where(fs_list_clean['계정'].isin(['자산', '지배기업주주지분']),
                                fs_list_clean['ttm'] / 4, fs_list_clean['ttm'])
fs_list_clean = fs_list_clean.groupby(['종목코드', '계정']).tail(1)

fs_list_pivot = fs_list_clean.pivot(index='종목코드', columns='계정', values='ttm')
fs_list_pivot['ROE'] = fs_list_pivot['지배주주순이익'] / fs_list_pivot['지배기업주주지분']
fs_list_pivot['GPA'] = fs_list_pivot['매출총이익'] / fs_list_pivot['자산']
fs_list_pivot['CFO'] = fs_list_pivot['영업활동으로인한현금흐름'] / fs_list_pivot['자산']


## 밸류
value_list.loc[value_list['값'] < 0, '값'] = np.nan
value_pivot = value_list.pivot(index = '종목코드', columns = '지표', values = '값')

## 모멘텀
price_pivot = price_list.pivot(index = '날짜', columns = '종목코드', values = '종가')

### 12개월 수익률
ret_list = pd.DataFrame(data = (price_pivot.iloc[-1] / price_pivot.iloc[0]) - 1, columns = ['12M'])

### K-Ratio
ret = price_pivot.pct_change().iloc[1: ]
ret_cum = np.log(1+ret).cumsum()

x = np.array(range(len(ret)))
k_ratio = {}
    
for i in range(0, len(ticker_list)) :    
    
    ticker = ticker_list.loc[i, '종목코드']    
    
    try:
        y = ret_cum.loc[:, price_pivot.columns == ticker]
        reg = sm.OLS(y, x).fit()
        res = float(reg.params / reg.bse)
    except:
        res = np.nan
        
    k_ratio[ticker] = res

k_ratio_bind = pd.DataFrame.from_dict(k_ratio, orient = 'index').reset_index()
k_ratio_bind.columns = ['종목코드', 'K_ratio']


# 데이터 합치기
data_bind = ticker_list[['종목코드', '종목명']].merge(sector_list[['CMP_CD', 'SEC_NM_KOR']], how = 'left', left_on = '종목코드', right_on = 'CMP_CD').\
    merge(fs_list_pivot[['ROE', 'GPA', 'CFO']], how = 'left', on = '종목코드').\
    merge(value_pivot, how = 'left', on = '종목코드').\
    merge(ret_list, how = 'left', on = '종목코드').\
    merge(k_ratio_bind, how = 'left', on = '종목코드')
    
data_bind.loc[data_bind['SEC_NM_KOR'].isnull(), 'SEC_NM_KOR'] = '기타'    
data_bind = data_bind.drop(['CMP_CD'], axis = 1)

data_bind.head()

# 그룹별 아웃라이어 제거한 후 랭킹과 Z-Score 구하기
data_bind_group = data_bind.set_index(['종목코드', 'SEC_NM_KOR']).groupby('SEC_NM_KOR')

## 아웃라이어 제거 기준 랭킹 구한 후 Z-Score 환산하는 함수
def col_clean(df, cutoff = 0.01, asc = False):
    
    q_low = df.quantile(cutoff)
    q_hi = df.quantile(1 - cutoff)
    
    df_trim = df[(df > q_low) & (df < q_hi)]
    
    if asc == False :    
        df_z_score = df_trim.rank(axis = 0, ascending = False).apply(zscore, nan_policy='omit')
    if asc == True :    
        df_z_score = df_trim.rank(axis = 0, ascending = True).apply(zscore, nan_policy='omit')
      
    
    return(df_z_score)

## 퀄리티

# data_bind['z_quality'] = data_bind_group[['ROE', 'GPA', 'CFO']].rank(axis = 0, ascending = False).groupby('SEC_NM_KOR').apply(zscore, nan_policy='omit').sum(axis = 1, skipna=False).values
z_quality = data_bind_group[['ROE', 'GPA', 'CFO']].apply(lambda x: col_clean(x, 0.01, False)).sum(axis = 1, skipna=False).to_frame('z_quality')
data_bind = data_bind.merge(z_quality, how = 'left', on = ['종목코드', 'SEC_NM_KOR'])

## 밸류

# value_1 = data_bind_group[['PBR', 'PCR', 'PER', 'PSR']].rank(axis = 0).groupby('SEC_NM_KOR').apply(zscore, nan_policy='omit')
#value_2 = data_bind_group[['DY']].rank(axis = 0, ascending = False).groupby('SEC_NM_KOR').apply(zscore, nan_policy='omit')
#data_bind['z_value'] = value_1.merge(value_2, on = ['종목코드', 'SEC_NM_KOR']).sum(axis = 1, skipna=False).values

value_1 = data_bind_group[['PBR', 'PCR', 'PER', 'PSR']].apply(lambda x: col_clean(x, 0.01, True))
value_2 = data_bind_group[['DY']].apply(lambda x: col_clean(x, 0.01, False))

z_value = value_1.merge(value_2, on = ['종목코드', 'SEC_NM_KOR']).sum(axis = 1, skipna=False).to_frame('z_value')
data_bind = data_bind.merge(z_value, how = 'left', on = ['종목코드', 'SEC_NM_KOR'])

## 모멘텀

# data_bind['z_momentum'] = data_bind_group[['12M', 'K_ratio']].rank(axis = 0, ascending = False).groupby('SEC_NM_KOR').apply(zscore, nan_policy='omit').sum(axis = 1, skipna=False).values
z_momentum = data_bind_group[['12M', 'K_ratio']].apply(lambda x: col_clean(x, 0.01, False)).sum(axis = 1, skipna=False).to_frame('z_momentum')
data_bind = data_bind.merge(z_momentum, how = 'left', on = ['종목코드', 'SEC_NM_KOR'])

# 분포 시각화
data_z = data_bind[['z_quality', 'z_value', 'z_momentum']].copy()

fig, axes = plt.subplots(3, 1, figsize=(10, 6), sharex=True, sharey = True)
for n, ax in enumerate(axes.flatten()):
    ax.hist(data_z.iloc[:, n])                   
    ax.set_title(data_z.columns[n], size = 12)
fig.tight_layout() 
plt.show()

# 다시 Z-Score 구하기
data_bind_final = data_bind[['종목코드', 'z_quality', 'z_value', 'z_momentum']].set_index('종목코드').apply(zscore, nan_policy='omit')
data_bind_final.columns = ['quality', 'value', 'momenmum']

fig, axes = plt.subplots(3, 1, figsize=(10, 6), sharex=True, sharey = True)
for n, ax in enumerate(axes.flatten()):
    ax.hist(data_bind_final.iloc[:, n])                   
    ax.set_title(data_bind_final.columns[n], size = 12)
fig.tight_layout() 
plt.show()


# 팩터 상관관계
import seaborn as sns

mask = np.triu(data_bind_final.corr())
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(data_bind_final.corr(), annot = True, mask = mask, annot_kws = {"size" : 16},
            vmin=0, vmax=1, center= 0.5, cmap= 'coolwarm', square = True)
ax.invert_yaxis()


# 비중만큼 곱한 뒤 합치기
wts = [0.3, 0.3, 0.3]
data_bind_final_sum = (data_bind_final * wts).sum(axis = 1, skipna=False).to_frame()
data_bind_final_sum.columns = ['qvm']
data_bind = data_bind.merge(data_bind_final_sum, on = '종목코드')

# 최종 종목
data_bind['invest'] = np.where(data_bind['qvm'].rank() <= 20, 'Y', 'N')
data_bind[data_bind['invest'] == 'Y']


#################

# 멜트 
data_melt = data_bind.melt(id_vars = 'invest', value_vars = ['ROE', 'GPA', 'CFO', 'PER', 'PBR', 'PCR', 'PSR', 'DY', '12M', 'K_ratio'])

# 함수
import seaborn as sns

def plot_rank(df):
    
    ax = sns.relplot(data = df, x = 'rank', y = 1, col = 'variable', hue = 'invest', style = 'invest',
                palette = ['grey', 'red'], size = 'invest', sizes = (100, 10), kind="scatter", col_wrap=3)
    ax.set(xlabel=None)
    ax.set(ylabel=None)
    
    sns.move_legend(
    ax, "lower center",
    bbox_to_anchor=(0.5, -.1), ncol=2)
    
    plt.show()


# 퀄리티 
hist_quality = data_melt[data_melt['variable'].isin(['ROE', 'GPA', 'CFO'])].copy()
hist_quality['rank'] = hist_quality.groupby('variable')['value'].rank(ascending = False)
plot_rank(hist_quality)

# 밸류
hist_value = data_melt[data_melt['variable'].isin(['PER', 'PBR', 'PCR', 'PSR', 'DY'])].copy()
hist_value['value'] = np.where(hist_value['variable'] == 'DY', 1/hist_value['value'], hist_value['value'])
hist_value['rank'] = hist_value.groupby('variable')['value'].rank()
plot_rank(hist_value)

# 모멘텀
hist_momentum = data_melt[data_melt['variable'].isin(['12M', 'K_ratio'])].copy()
hist_momentum['rank'] = hist_momentum.groupby('variable')['value'].rank(ascending = False)
plot_rank(hist_momentum)
