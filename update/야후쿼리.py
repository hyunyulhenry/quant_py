# https://yahooquery.dpguthrie.com/

from yahooquery import Ticker
import pandas as pd
import numpy as np

ticker = 'appl'
aapl = Ticker('AAPL')
aapl.asset_profile
aapl.summary_detail
aapl.calendar_events
aapl.price

aapl.history(start = '2000-01-01')

bs_y = aapl.balance_sheet(frequency = 'a')
bs_q = aapl.balance_sheet(frequency = 'q', trailing = False)

cf_y = aapl.cash_flow(frequency = 'a', trailing = False)
cf_q = aapl.cash_flow(frequency = 'q', trailing = False)

is_y = aapl.income_statement(frequency = 'a', trailing = False)
is_q = aapl.income_statement(frequency = 'q', trailing = False)

# 연간
data_fs_y = aapl.all_financial_data(frequency = 'a')
data_fs_y.reset_index(inplace = True)
data_fs_y = data_fs_y.loc[:, ~data_fs_y.columns.isin(['periodType', 'currencyCode'])]
data_fs_y = data_fs_y.melt(id_vars = ['symbol', 'asOfDate'])
data_fs_y = data_fs_y.replace([np.nan], None)
data_fs_y['freq'] = 'y'
data_fs_y.columns = ['ticker', 'date', 'account', 'value', 'freq']

# 인덱스를 일반 열로
# 12M 이면 'y' 3M 이면 'q'
# 통화 없애기
# 피벗 걸기
# nan -> None 으로

# 분기
data_fs_q = aapl.all_financial_data(frequency = 'q')
data_fs_q.reset_index(inplace = True)
data_fs_q = data_fs_q.loc[:, ~data_fs_q.columns.isin(['periodType', 'currencyCode'])]
data_fs_q = data_fs_q.melt(id_vars = ['symbol', 'asOfDate'])
data_fs_q = data_fs_q.replace([np.nan], None)
data_fs_q['freq'] = 'q'
data_fs_q.columns = ['ticker', 'date', 'account', 'value', 'freq']

# 합치기
data_fs = pd.concat([data_fs_y, data_fs_q])