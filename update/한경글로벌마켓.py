market = 'nyse'
# 나스닥: nasdaq
# 아멕스: amex
url = f'''https://www.hankyung.com/globalmarket/data/price?type={market}\
&sort=market_cap_top&sector_nm=&industry_nm=&chg_net_text='''
    
import json
import requests as rq    
import pandas as pd

data = rq.get(url).json()

data_pd = pd.json_normalize(data['list'])
data_pd['symbol'] = data_pd['symbol'].str.replace('-US', '')
data_pd['symbol'] = data_pd['symbol'].str.replace('.', '-')

