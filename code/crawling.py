import pandas as pd

url = 'https://en.wikipedia.org/wiki/List_of_countries_by_stock_market_capitalization'

tbl = pd.read_html(url)

tbl[0]