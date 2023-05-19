
# https://pypi.org/project/tiingo/

from tiingo import TiingoClient
import pandas as pd

api_key = '88b094a745a1355cd76a4f956931aa702cf0e852'

config = {}
config['session'] = True
config['api_key'] = api_key
client = TiingoClient(config)

# 티커 정보
tickers = client.list_stock_tickers()
tickers_df = pd.DataFrame.from_records(tickers)
tickers_df.groupby(['exchange', 'priceCurrency'])['ticker'].count()

# meta data
ticker_metadata = client.get_ticker_metadata("AAPL")
print(ticker_metadata)

# price
historical_prices = client.get_dataframe("AAPL",
                                         startDate='2017-08-01',
                                         frequency='daily')

historical_prices['adjClose'].plot()

# fs definitions
definitions = client.get_fundamentals_definitions('GOOGL')
definitions_df = pd.DataFrame.from_records(definitions)
definitions_df.head()

# 일별 fundamental
# (무료의 경우 Dow 30 종목만 제공)
fundamentals_daily = client.get_fundamentals_daily('AAPL')
fundamentals_daily_df = pd.DataFrame.from_records(fundamentals_daily)                                           

# 재무제표
fundamentals_stmnts = client.get_fundamentals_statements('AAPL',
                                                         startDate='2000-01-01',
                                                         asReported=True,
                                                         fmt = 'csv')

df_fs = pd.DataFrame([x.split(',') for x in fundamentals_stmnts.split('\n')])
df_fs.columns = df_fs.iloc[0] 
df_fs = df_fs[1:]
df_fs.set_index('date', drop = True, inplace = True)
df_fs = df_fs[df_fs.index != '']
