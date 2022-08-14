#!/usr/bin/env python
# coding: utf-8

# # 전 세계 주식 데이터 수집하기
# 
# 퀀트 투자의 장점은 데이터만 있다면 동일한 투자 전략을 전 세계 모든 국가에 적용할 수 있다는 점이다. 이번 장에서는 전 세계 종목의 티커 수집 및 주가, 재무제표, 가치지표를 다운로드 하는 방법에 대해 알아보겠다.
# 
# ## 유료 데이터 벤더 이용하기
# 
# 미국 시장의 데이터만 필요할 경우 유료 데이터 벤더를 이용하는 것도 좋은 방법이다. 미국에는 금융 데이터를 API로 제공하는 수많은 업체가 있으며, tiingo의 경우는 월 $10만 지불하면 미국과 중국의 4만여개 종목에 대한 데이터를 API 형태로 받을 수 있다. 이는 상장폐지된 종목을 커버할 뿐만 아니라, API를 이용하므로 크롤링과는 비교할 수 없는 속도로 데이터를 받을 수 있다는 장점이 있다. 이 외에도 Alpha Vantage, Quandl, Polygon 등 수많은 데이터 벤더가 존재한다.
# 
# ```{figure} image/data_global/tiingo.png
# ---
# scale: 70%
# name: tiingo
# ---
# tiingo의 유/무료 서비스 비교
# ```
# 
# tiingo는 무료 계정도 하루 1,000회까지 API 요청을 할 수 있으며, 파이썬에서 사용할 수 있는 패키지도 있으므로 이를 사용해 데이터를 수집해보도록 하겠다. 
# 
# ### 가입 및 API token 받기
# 
# 먼저 https://api.tiingo.com/ 사이트에 접속하여 우측 상단의 [Sign-up]을 클릭해 회원가입을 한다. 그 후 로그인을 한 후 우측 상단에서 본인의 ID를 클릭한 후 [Account]를 선택, 좌측 메뉴의 [API] 부분에서 [Token]을 클릭하면 본인의 API token을 확인할 수 있다.
# 
# ```{figure} image/data_global/token.png
# ---
# name: token
# ---
# API token 확인
# ```
# 
# 발급받은 토큰을 PC에 저장할 경우, keyring 패키지를 이용하면 안전하게 저장할 수 있다. 패키지를 이용해 암호나 키 값을 저장하는 법은 다음과 같다.

# In[ ]:


import keyring

keyring.set_password('System', 'User Name', 'Password')


# [System]에는 시스템 종류, [User Name]에는 본인의 이름, [Password]에는 발급받은 API Key를 입력한다. 한번 입력된 값은 계속 저장되어 있다. 저장한 키를 불러오는 법은 다음과 같다.

# In[ ]:


api_key = keyring.get_password('System', 'User Name')


# 이제 'Sysyem'에는 'tiingo', 'User Name'에는 본인의 이름, 'Password'에는 위에서 발급받은 API Token을 입력해 토큰을 저장하자.

# In[ ]:


import keyring

keyring.set_password('tiingo', 'User Name', 'Your API Token')


# ### 데이터 다운로드
# 
# tiingo 패키지를 이용해 데이터를 받아보도록 하겠다. 데이터를 받기위해 API 접속환경을 셋팅한다.

# In[1]:


from tiingo import TiingoClient
import pandas as pd
import keyring

api_key = keyring.get_password('tiingo', 'Henry')
config = {}
config['session'] = True
config['api_key'] = api_key
client = TiingoClient(config)


# API token을 불러온 후, 접속환경에 해당하는 config에 이를 입력한다.
# 
# 먼저 tiingo에서 제공하는 종목은 어떠한 것이 있는지 티커 정보들을 확인해보도록 하자.

# In[2]:


tickers = client.list_stock_tickers()
tickers_df = pd.DataFrame.from_records(tickers)

tickers_df.head()


# `list_stock_tickers()` 메서드를 통해 티커 정보를 받아올 수 있다. ticker(티커), exchange(거래소), assetType(주식 종류), priceCurrency(거래 통화), startDate(시작일), endDate(마감일) 정보가 표시된다. 거래소와 통화 별 종목이 몇개가 있는지 확인해보도록 하자.

# In[3]:


tickers_df.groupby(['exchange', 'priceCurrency'])['ticker'].count()


# 이 중 마이너 거래소나 장외 거래소의 경우 정보를 받아도 우리나라의 증권사를 통해서는 실제로 거래를 할 수 없을수도 있다. 따라서 실제 거래가 가능한 거래소 데이터만 필터링한 후 해당 종목들을 받는 것이 효율적이다.
# 
# 각 종목의 상세 정보를 확인해보도록 하며, 예로써 애플(AAPL)을 이용한다.

# In[4]:


ticker_metadata = client.get_ticker_metadata("AAPL")
print(ticker_metadata)


# `get_ticker_metadata()` 메서드 내에 티커를 입력하면 티커, 종목명, 사업내역 등 대략적인 정보를 받아올 수 있다.
# 
# 이제 주가를 받아보도록 하자.

# In[5]:


historical_prices = client.get_dataframe("AAPL",
                                         startDate='2017-08-01',
                                         frequency='daily')

historical_prices.head()


# `get_dataframe()` 메서드 내에 티커를 입력하면 close(종가), high(고가), low(저가), open(시가), volumne(거래량) 및 수정주가와 divCash(현금 배당), splitFactor(주식분할 조정계수)까지 데이터를 받을 수 있다.
# 
# 이번에는 일별 가치지표를 받아보도록 하자. (무료 계정의 경우 다우존스 30 지수에 포함되는 종목 정보만 제공한다.)

# In[7]:


fundamentals_daily = client.get_fundamentals_daily('AAPL')
fundamentals_daily_df = pd.DataFrame.from_records(fundamentals_daily)

fundamentals_daily_df.head()


# `get_fundamentals_daily()` 메서드 내에 티커를 입력하면 일간 시가총액, 기업가치, PER, PBR, PEG 정보가 JSON 형태로 받아지며, `from_records()` 메서드를 통해 데이터프레임 형태로 변경해준다.
# 
# 마지막으로 재무제표를 받아보도록 하자.

# In[8]:


fundamentals_stmnts = client.get_fundamentals_statements(
    'AAPL', startDate='2019-01-01', asReported=True, fmt='csv')

df_fs = pd.DataFrame([x.split(',') for x in fundamentals_stmnts.split('\n')])
df_fs.columns = df_fs.iloc[0]
df_fs = df_fs[1:]
df_fs.set_index('date', drop=True, inplace=True)
df_fs = df_fs[df_fs.index != '']

df_fs.head()


# 1. `get_fundamentals_statements()` 메서드 내에 티커를 입력하면 재무제표의 세부항목을 받을 수 있다. 또한 `fmt`은 포맷 형태를 의미하며, JSON으로 받을 경우 형태가 지나치게 복잡하므로 CSV로 받는 것이 좋다.
# 2. 텍스트 형태로 데이터가 들어오므로, 클렌징을 통해 데이터프레임 형태로 변경한다.
# 3. 첫번째 행을 열 이름으로 지정한 후, 해당 행은 삭제한다.
# 4. 'date' 열을 인덱스로 지정한다.
# 5. 'date'가 비어있는 부분이 있으므로 이를 제거한다.
# 
# 결과를 확인해보면 연간 재무제표와 분기 재무제표의 상세 정보가 다운로드 될 뿐만 아니라 발표 날짜 또한 제공된다. 이처럼 유료 벤더를 이용하면 티커 및 주가, 재무제표, 가치지표를 매우 쉽고 빠르게 받을 수 있다. 
# 
# tiingo의 API 사용법 및 파이썬 패키지 사용법은 아래 페이지에 나와있다.
# 
# - tiingo API: https://api.tiingo.com/documentation/general/overview
# - 파이썬 패키지: https://github.com/hydrosquall/tiingo-python
# 
# ## 티커 수집하기
# 
# 이번에는 크롤링을 통해 데이터를 수집하는 방법에 대해 알아보겠다. 우리나라는 한국거래소를 통해 티커를 손쉽게 수집할 수 있지만 해외의 경우는 그렇지 않다. 먼저 우리나라와 달리 국가 별로 거래소가 여러개인 경우도 있으며, 홈페이지에 상장 종목 리스트를 제공하지 않는 경우도 많기 때문이다. 
# 
# 다행히 투자자들이 많이 참조하는 사이트인 인베스팅닷컴(https://www.investing.com/)에서는 전 세계 주식 및 각종 금융 데이터를 제공하고 있다. 이 중 스크리닝 기능을 활용하면 각 국가별 티커 리스트를 수집할 수 있다. 먼저 인베스팅닷컴에 접속한 후 [Markets → Stocks → Stock Screener]에 접속한다.
# 
# ```{figure} image/data_global/screen.png
# ---
# name: screen
# ---
# 인베스팅닷컴의 주식 스크리너
# ```
# 
# 페이지를 접속하면 미국 종목들이 나타나며, URL은 다음과 같다. 
# 
# ```
# https://www.investing.com/stock-screener/?sp=country::5|sector::a|industry::a|equityType::a%3Ceq_market_cap;1
# ```
# 
# 하단에 표로 나타는 정보 중 Symbol이 티커에 해당하며, 이를 통해 티커를 손쉽게 수집할 수 있다. 다음으로 국가를 Japan(일본)으로 선택하고, Equity Type은 ORD(보통주)를 선택하자.
# 
# ```{figure} image/data_global/japan.png
# ---
# name: japan
# ---
# 일본 국가 선택
# ```
# 
# 하단의 테이블이 일본 종목들로 바뀌며 URL 역시 다음과 같이 바뀐다.
# 
# ```
# https://www.investing.com/stock-screener/?sp=country::35|sector::a|industry::a|equityType::ORD%3Ceq_market_cap;1
# ```
# 
# 즉 기존 URL 중 국가에 해당하는 'country' 부분이 5에서 35로, 주식 종류에 해당하는 'equityType' 부분이 a에서 ORD로 변경되었다. 해당 페이지는 동적으로 페이지가 바뀌므로 셀레니움을 통해 크롤링을 해야한다. 예제로 미국의 보통주 전종목 정보를 크롤링 해보도록 하자.

# In[9]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import math
import pandas as pd

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = 'https://www.investing.com/stock-screener/?sp=country::5|sector::a|industry::a|equityType::ORD%3Ceq_market_cap;1'
driver.get(url)


# 1. 먼저 크롬 드라이버를 설정한다.
# 2. 미국 보통주에 해당하는 URL을 입력한다.
# 3. 해당 페이지를 연다.
# 
# ```{figure} image/data_global/selenium_open.png
# ---
# name: selenium_open
# ---
# 셀레니움을 이용한 스크리너 접속
# ```
# 
# 다음으로 HTML 정보를 가져오도록 한다.

# In[10]:


html = BeautifulSoup(driver.page_source, 'lxml')


# HTML 정보에 해당하는 `driver.page_source`를 BeautifulSoup 객체로 만들어준다. 이제 우리가 찾고자 하는 데이터를 하나씩 살펴보도록 한다. 먼저 각 국가별 코드를 살펴보도록 하자. 개발자도구 화면에서 'newBtnDropdown noHover' 클래스 하단의 'li 태그의 'data-value' 속성을 살펴보면 국가별 코드와 국가명이 적혀있다.
# 
# ```{figure} image/data_global/country_ticker.png
# ---
# name: country_ticker
# ---
# 국가별 코드
# ```
# 
# 이번에는 위젯에서 선택되어 있는 국가명을 확인해보도록 하자. 'newBtnDropdown noHover' 클래스 하단의 'input' 태그의 'value' 속성의 속성명에는 국가명이 적혀 있다. 이를 코드를 통해 찾아보도록 하자.
# 
# ```{figure} image/data_global/country_name.png
# ---
# name: country_name
# ---
# 국가명 확인
# ```

# In[11]:


html.find(class_='js-search-input inputDropDown')['value']


# 이번에는 종목들의 정보가 있는 테이블을 확인해보도록 하자. 클래스 명이 'genTbl openTbl resultsStockScreenerTbl elpTbl' 인 테이블 중 'tbody' 부분에 해당 데이터가 위치하고 있다. 이 정보를 이용해 해당 테이블 데이터를 선택하자.
# 
# ```{figure} image/data_global/screen_table.png
# ---
# name: screen_table
# ---
# 종목 테이블
# ```

# In[12]:


html_table = html.select('table.genTbl.openTbl.resultsStockScreenerTbl.elpTbl')


# In[ ]:


print(html_table[0])


# ```{figure} image/data_global/selenium_1.png
# ---
# name: selenium_1
# ---
# ```
# 
# `select` 함수를 이용해 table 태그 중 해당 클래스명을 찾은 후 출력하면, 종목 정보들이 담긴 테이블의 HTML 정보가 출력된다. 이제 이를 데이터프레임 형태로 변환해보도록 하자.

# In[13]:


df_table = pd.read_html(html_table[0].prettify())
df_table_result = df_table[0]


# `prettify()` 메서드를 이용해 BeautifulSoup 에서 파싱한 파서 트리를 유니코드 형태로 다시 돌려준 후, `read_html()` 함수를 통해 테이블을 읽어온다. Variable Explorer 창에서 df_table_result 변수를 확인해보자.
# 
# ```{figure} image/data_global/selenium_2.png
# ---
# name: selenium_2
# ---
# 크롤링 결과 확인
# ```
# 
# 결과를 살펴보면 웹페이지에 있는 내역 외에도 Exchange(거래소), Sector, Industy 등 추가적인 정보를 확인할 수 있다. 이 중 필요한 열만 선택하자.

# In[14]:


df_table_select = df_table[0][['Name', 'Symbol', 'Exchange',  'Sector', 'Market Cap']]
df_table_select.head()


# 마지막으로 종목 정보가 몇페이지까지 있는지 확인해야 한다. 웹페이지의 'Screener Results' 글자 뒤에는 해당 국가에 총 몇 종목이 있는지 출력된다. 한 페이지에는 총 50 종목이 출력되므로 해당 숫자를 50으로 나눈 후 올림을 하면 총 페이지 수를 계산할 수 있다. 해당 정보는 'js-total-results' 클래스에 위치하고 있으며, 이를 이용해 페이지 수를 계산해보도록 하자.
# 
# ```{figure} image/data_global/country_page.png
# ---
# name: country_page
# ---
# 종목 수 확인
# ```

# In[15]:


end_num = driver.find_element(By.CLASS_NAME, value = 'js-total-results').text
print(math.ceil(int(end_num) / 50))


# 마지막으로 드라이브롤 종료해준다.

# In[16]:


driver.quit()


# ### 전 종목 티커 크롤링
# 
# 위 과정을 통해 국가별 전 종목의 티커 및 관련 정보를 수집하는 방법과, 페이지 수를 계산할 수 있었다. 이제 for문을 이용해 미국의 전 종목 티커를 크롤링해보도록 하겠다.

# In[25]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from datetime import datetime
import math
import pandas as pd
import numpy as np
from tqdm import tqdm
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
nationcode = '5'
url = f'''https://investing.com/stock-screener/?sp=country::
{nationcode}|sector::a|industry::a|equityType::ORD%3Ceq_market_cap;1'''
driver.get(url)

WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
    (By.XPATH, '//*[@id="resultsTable"]/tbody')))

end_num = driver.find_element(By.CLASS_NAME, value='js-total-results').text
end_num = math.ceil(int(end_num) / 50)


# 1. 크롬 드라이브를 불러온다.
# 2. 국가 코드는 미국에 해당하는 '5'를 입력한다.
# 3. 먼저 첫페이지에 해당하는 URL을 생성한다.
# 4. 셀레니움으로 해당 페이지를 연다
# 5. 'Screener Results'에 해당하는 부분은 종목이 들어있는 테이블이 로딩된 이후 나타난다. 따라서 `WebDriverWait()` 함수를 통해 해당 테이블이 로딩될 때까지 기다리며, 테이블의 XPATH는 '//*[@id="resultsTable"]/tbody' 이다.
# 6. 종목수에 해당하는 부분을 크롤링한 후, 이를 통해 페이지 수를 계산한다.
# 
# 이제 for문을 통해 모든 페이지의 데이터를 크롤링해보도록 하자.

# In[ ]:


all_data_df = []

for i in tqdm(range(1, end_num + 1)):

    url = f'''https://investing.com/stock-screener/?sp=country::
        {nationcode}|sector::a|industry::a|equityType::ORD%3Ceq_market_cap;{i}'''
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="resultsTable"]/tbody')))
    except:
        time.sleep(1)
        driver.refresh()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="resultsTable"]/tbody')))

    html = BeautifulSoup(driver.page_source, 'lxml')

    html_table = html.select(
        'table.genTbl.openTbl.resultsStockScreenerTbl.elpTbl')
    df_table = pd.read_html(html_table[0].prettify())
    df_table_select = df_table[0][['Name', 'Symbol',
                                   'Exchange',  'Sector', 'Market Cap']]

    all_data_df.append(df_table_select)

    time.sleep(2)

all_data_df_bind = pd.concat(all_data_df, axis=0)

data_country = html.find(class_='js-search-input inputDropDown')['value']
all_data_df_bind['country'] = data_country
all_data_df_bind['date'] = datetime.today().strftime('%Y-%m-%d')
all_data_df_bind = all_data_df_bind[~all_data_df_bind['Name'].isnull()]
all_data_df_bind = all_data_df_bind[all_data_df_bind['Exchange'].isin(
    ['NASDAQ', 'NYSE', 'NYSE Amex'])]
all_data_df_bind = all_data_df_bind.drop_duplicates(['Symbol'])
all_data_df_bind.reset_index(inplace=True, drop=True)
all_data_df_bind = all_data_df_bind.replace({np.nan: None})

driver.quit()


# 1. 빈 리스트(all_data_df)를 생성한다.
# 2. for문을 통해 전체 페이지에서 종목명과 티커 등의 정보를 크롤링한다.
# 3. f-string을 통해 각 페이지에 해당하는 URL을 생성한 후 페이지를 연다.
# 4. `WebDriverWait()` 함수를 통해 테이블이 로딩될때 까지 기다린다. 또한 간혹 페이지 오류가 발생할 때가 있으므로, try except문을 이용해 오류 발생 시 1초간 기다린 후 `refresh()`를 통해 새로고침을 하여 다시 테이블이 로딩되길 기다린다.
# 5. HTML 정보를 불러온 후, 테이블에 해당하는 부분을 선택한다.
# 6. 원하는 열만 선택한다.
# 7. `append()` 메서드를 통해 해당 테이블을 리스트에 추가한다.
# 8. 2초가 일시정지를 한다.
# 9. for문이 끝나면 `concat()` 함수를 통해 리스트 내 모든 데이터프레임을 행으로 묶어준다.
# 10. 국가명에 해당하는 부분을 추출한 뒤, 'country' 열에 입력한다.
# 11. 'date' 열에 오늘 날짜를 입력한다.
# 12. 일부 종목의 경우 종목명이 빈칸으로 들어오므로 이를 제거한다.
# 13. 'Exchange' 열에서 거래가 가능한 거래소만 선택한다.
# 14. 일부 종목의 경우 중복된 결과가 들어오기도 하므로 `drop_duplicates()` 메서드를 통해 Symbol이 겹치는 경우 한개만 남겨준다.
# 14. `reset_index()` 메서드를 통해 인덱스를 초기화한다.
# 15. nan을 None으로 변경한다.
# 16. 드라이브롤 종료한다.
# 
# 마지막으로 위 데이터프레임을 SQL에 저장해주도록 한다. 먼저 SQL에서 다음의 쿼리를 통해 테이블(global_ticker)을 만든다.

# In[ ]:


use stock_db;

create table global_ticker
(
    Name varchar(50) not null,
    Symbol varchar(30),
    Exchange varchar(30),
    Sector varchar(30),
    `Market Cap` varchar(10),
    country varchar(20),    
    date date,
    primary key(Symbol, country, date)
);


# 위에서 구한 티커 데이터를 해당 테이블에 저장한다.

# In[ ]:


import pymysql

con = pymysql.connect(user='root',
                      passwd='1234',
                      host='127.0.0.1',
                      db='stock_db',
                      charset='utf8')

mycursor = con.cursor()
query = """
    insert into global_ticker (Name, Symbol, Exchange, Sector, `Market Cap`, country, date)
    values (%s,%s,%s,%s,%s,%s,%s) as new
    on duplicate key update
    name=new.name,Exchange=new.Exchange,Sector=new.Sector,
    `Market Cap`=new.`Market Cap`; 
"""

args = all_data_df_bind.values.tolist()

mycursor.executemany(query, args)
con.commit()

con.close()


# ```{figure} image/data_global/ticker_sql.png
# ---
# name: ticker_sql
# ---
# 글로벌 티커 테이블
# ```
# 
# ```{note}
# - nationcode 부분만 변경하면 모든 국가의 티커 리스트 역시 동일한 방법으로 다운로드 받을 수 있다.
# ```
# 
# ## 주가 다운로드
# 
# 야후 파이낸스에서는 전 세계 주가(한국 포함)를 제공하고 있다.
# 
# ```
# https://finance.yahoo.com/
# ```
# 
# 사이트에서 종목 티커를 검색한 후 [Historical Data] 탭을 선택하면 확인 및 다운로드가 가능하다. 또한 pandas_datareader 패키지의 `DataReader()` 함수를 사용하면 야후 API를 통해 해당 데이터를 매우 손쉽게 다운로드 받을 수도 있다. 예시로써 애플(AAPL)의 주가를 다운로드 받아보도록 하자.
# 
# ```{figure} image/data_global/yahoo_price.png
# ---
# name: yahoo_price
# ---
# 야후에서 제공하는 주가 데이터
# ```

# In[17]:


import pandas_datareader as web

price = web.DataReader('AAPL', 'yahoo')
price.head()


# `DataReader()` 함수 내에 티커와 출처에 해당하는 'yahoo'를 입력하면 주가 정보를 매우 손쉽게 받을 수 있다.
# 
# 반면 미국이 아닌 국가의 경우 단순히 티커만 입력할 경우 데이터를 받을 수 없다. 예를 들어 일본의 '도쿄 일렉트론'은 일본 내에서 티커가 '8035'이며, 야후 파이낸스에서 이를 검색해보자.
# 
# ```{figure} image/data_global/same_ticker.png
# ---
# name: same_ticker
# ---
# 중복 티커
# ```
# 
# 우리가 원하는 도쿄 일렉트론 뿐만 아니라 홍콩에 상장된 'Janco Holdings Limited'라는 주식 역시 티커가 8035 이다. 이처럼 각기 다른 국가에서 중복된 티커가 사용되는 경우가 종종 발생되므로, 야후 파이낸스 혹은 여러 벤더의 경우 '티커.국가코드' 형태를 통해 이들을 구분한다. 야후 파이낸스에서 일본의 국가코드는 'T' 이다. 이를 이용해 도쿄 일렉트론의 주가를 받는 법은 다음과 같다.

# In[18]:


import pandas_datareader as web

price = web.DataReader('8035.T', 'yahoo')
price.head()


# ```{note}
# - 미국의 경우는 국가코드가 필요없이 단순히 티커만 입력하면 된다.
# - 국내 주가 역시 야후 파이낸스를 통해 다운로드 받을 수 있다. 그러나 일부 중소형주의 경우 데이터가 존재하지 않는 문제가 있어 국내 사이트를 이용해 수집하는 것을 권장한다.
# ```
# 
# ### 전 종목 주가 다운로드
# 
# 미국 데이터 역시 국내 전종목 주가를 다운로드 받고 DB에 저장했던것과 동일하게 for문을 이용하면 된다. 먼저 SQL에서 주가 데이터에 해당하는 테이블(global_price)를 만든다.

# In[ ]:


use stock_db;

create table global_price
(
    Date date,
    High double,
    Low double,
    Open double,
    Close double,
    Volume double,
    `Adj Close` double,
    ticker varchar(20),
    primary key(Date, ticker)
);


# 파이썬에서 아래 코드를 실행하면 for문을 통해 전종목 주가가 DB에 저장된다.

# In[ ]:


# 패키지 불러오기
import pymysql
from sqlalchemy import create_engine
import pandas as pd
import pandas_datareader as web
import time
from tqdm import tqdm

# DB 연결
engine = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/stock_db')
con = pymysql.connect(user='root',
                      passwd='1234',
                      host='127.0.0.1',
                      db='stock_db',
                      charset='utf8')

mycursor = con.cursor()

# 티커리스트 불러오기
ticker_list = pd.read_sql("""
select * from global_ticker
where date = (select max(date) from global_ticker)
and country = 'United States';
""", con=engine)

# DB 저장 쿼리
query = """
    insert into global_price (Date, High, Low, Open, Close, Volume, `Adj Close`, ticker)
    values (%s, %s,%s,%s,%s,%s,%s,%s) as new
    on duplicate key update
    High = new.High, Low = new.Low, Open = new.Open, Close = new.Close,
    Volume = new.Volume, `Adj Close` = new.`Adj Close`;
"""

# 오류 발생시 저장할 리스트 생성
error_list = []

# 전종목 주가 다운로드 및 저장
for i in tqdm(range(0, len(ticker_list))):

    # 티커 선택
    ticker = ticker_list['Symbol'][i]

    # 오류 발생 시 이를 무시하고 다음 루프로 진행
    try:

        # url 생성
        price = web.DataReader(ticker, 'yahoo')

        # 데이터 클렌징
        price = price.reset_index()
        price['ticker'] = ticker

        # 주가 데이터를 DB에 저장
        args = price.values.tolist()
        mycursor.executemany(query, args)
        con.commit()

    except:

        # 오류 발생시 error_list에 티커 저장하고 넘어가기
        print(ticker)
        error_list.append(ticker)

    # 타임슬립 적용
    time.sleep(2)

# DB 연결 종료
engine.dispose()
con.close()


# 1. DB에 연결한다.
# 2. 기준일이 최대, 즉 최근일 기준 보통주에 해당하며, 미국 종목의 리스트(ticker_list)만 불러온다.
# 3. DB에 저장할 쿼리(query)를 입력한다.
# 4. 페이지 오류, 통신 오류 등 오류가 발생한 티커명을 저장할 리스트(error_list)를 만든다.
# 5. for문을 통해 전종목 주가를 다운로드 받으며, 진행상황을 알기위해 `tqdm()` 함수를 이용한다.
# 6. `DataReader()` 함수를 통해 야후 파이낸스에서 주가를 받은 후 클렌징 처리한다. 그 후 주가 데이터를 DB에 저장한다.
# 7. try except문을 통해 오류가 발생시 'error_list'에 티커를 저장한다.
# 8. 무한 크롤링을 방지하기 위해 한 번의 루프가 끝날 때마다 타임슬립을 적용한다.
# 9. 모든 작업이 끝나면 DB와의 연결을 종료한다.
# 
# ```{figure} image/data_global/sql_price.png
# ---
# name: sql_price
# ---
# 글로벌 주가 테이블
# ```
# 
# 작업이 종료된 후 'error_list'에는 오류가 발생해 다운로드 받지 못한 종목들이 입력되어 있다. 이는 페이지 오류나 통신 오류 때문일 수도 있으며, 인베스팅닷컴에는 존재하지만 야후 파이낸스에는 존재하지 않는 종목일 수도 있다.
# 
# ```{note}
# 미국이 아닌 타 국가의 경우 티커의 중복 방지를 위해 ticker 열에 국가코드도 함께 입력한 후 DB에 저장하는 것을 추천한다.
# ```
# 
# ## 재무제표 다운로드
# 
# 재무제표 역시 야후 파이낸스에서 구할 수 있으며, [Financials] 탭을 클릭하면 연간 및 분기 기준 재무제표를 제공하고 있다. 해당 데이터를 다운로드 받을 수 있는 여러 패키지가 존재하며, 본 책에서는 그 중에서도 yahoo_fin 패키지를 사용하도록 하겠다. 해당 패키지의 자세한 설명은 아래 사이트에서 확인할 수 있다.
# 
# ```
# http://theautomatic.net/yahoo_fin-documentation/
# ```
# 
# ```{figure} image/data_global/yahoo_fs.png
# ---
# name: yahoo_fs
# ---
# 야후에서 제공하는 재무제표 데이터
# ```
# 
# 해당 패키지의 `get_financials()` 함수를 이용하면 손익계산서, 재무상태표, 현금흐름표를 한번에 다운로드 받을 수 있으며, 예시로 애플(AAPL) 종목의 연간 재무제표를 받아보도록 하겠다.

# In[19]:


import yahoo_fin.stock_info as si

data_y = si.get_financials('AAPL', yearly=True, quarterly=False)
data_y.keys()


# 인자의 `yearly = True, quarterly = False`는 연간 재무제표를 의미하며, 딕셔너리 형태로 세 종류의 재무제표가 다운로드 되었다. 이를 하나의 데이터프레임으로 합쳐주도록 한다.

# In[20]:


import pandas as pd

data_fs_y = pd.concat([v for k, v in data_y.items()])
data_fs_y = data_fs_y.stack().reset_index()
data_fs_y.columns = ['account', 'date', 'value']
data_fs_y['freq'] = 'y'

data_fs_y.head()


# 1. 딕셔너리의 value에 해당하는 부분만을 선택한 후 `concat()` 함수를 통해 데이터프레임 형태로 합쳐준다.
# 2. `stack()` 함수를 통해 데이터를 위에서 아래로 길게 재구조화 해주며, `reset_index()`를 통해 인덱스를 초기화한다.
# 3. 열 이름을 변경한다.
# 4. freq 열에 연간에 해당하는 'y'를 입력한다.
# 
# 이처럼 패키지를 이용하여 미국 재무제표 데이터도 매우 쉽게 다운로드 받을 수 있다. 분기별 재무제표를 받는법도 위와 같으며, 인자만 `yearly=False, quarterly=True`로 변경하면 된다.

# In[21]:


data_q = si.get_financials('AAPL', yearly=False, quarterly=True)
data_fs_q = pd.concat([v for k, v in data_q.items()])
data_fs_q = data_fs_q.stack().reset_index()
data_fs_q.columns = ['account', 'date', 'value']
data_fs_q['freq'] = 'q'

data_fs_q.head()


# ### 전 종목 재무제표 다운로드
# 
# for문을 이용하여 전 종목 재무제표를 다운로드 받도록 하겠다. 먼저 SQL에서 재무제표 데이터에 해당하는 테이블(global_fs)를 만든다.

# In[ ]:


use stock_db;

create table global_fs
(
    account varchar(100),
    date date,
    value double,
    freq varchar(1),
    ticker varchar(20),    
    primary key(account, date, ticker, freq)
);


# 이제 파이썬에서 아래 코드를 실행하면 for문을 통해 전 종목 재무제표가 DB에 저장된다.

# In[ ]:


# 패키지 불러오기
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import yahoo_fin.stock_info as si
import time
from tqdm import tqdm

# DB 연결
engine = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/stock_db')
con = pymysql.connect(user='root',
                      passwd='1234',
                      host='127.0.0.1',
                      db='stock_db',
                      charset='utf8')

mycursor = con.cursor()

# 티커리스트 불러오기
ticker_list = pd.read_sql("""
select * from global_ticker
where date = (select max(date) from global_ticker)
and country = 'United States';
""", con=engine)

# DB 저장 쿼리
query_fs = """
    insert into global_fs (account, date, value, freq, ticker)
    values (%s,%s,%s,%s,%s) as new
    on duplicate key update
    value = new.value;
"""

# 오류 발생시 저장할 리스트 생성
error_list = []

# 전종목 주가 다운로드 및 저장
for i in tqdm(range(0, len(ticker_list))):

    # 티커 선택
    ticker = ticker_list['Symbol'][i]

    # 오류 발생 시 이를 무시하고 다음 루프로 진행
    try:

        # 재무제표 다운로드
        data_y = si.get_financials(ticker, yearly=True, quarterly=False)
        data_fs_y = pd.concat([v for k, v in data_y.items()])
        data_fs_y = data_fs_y.stack().reset_index()
        data_fs_y.columns = ['account', 'date', 'value']
        data_fs_y['freq'] = 'y'

        data_q = si.get_financials('AAPL', yearly=False, quarterly=True)
        data_fs_q = pd.concat([v for k, v in data_q.items()])
        data_fs_q = data_fs_q.stack().reset_index()
        data_fs_q.columns = ['account', 'date', 'value']
        data_fs_q['freq'] = 'q'

        data_fs = pd.concat([data_fs_y, data_fs_q], axis=0)
        data_fs['ticker'] = ticker

        # 주가 데이터를 DB에 저장
        args = data_fs.values.tolist()
        mycursor.executemany(query_fs, args)
        con.commit()

    except:

        # 오류 발생시 error_list에 티커 저장하고 넘어가기
        print(ticker)
        error_list.append(ticker)

    # 타임슬립 적용
    time.sleep(2)

# DB 연결 종료
engine.dispose()
con.close()


# 1. DB에 연결한다.
# 2. 기준일이 최대, 즉 최근일 기준 보통주에 해당하며, 미국 종목의 리스트(ticker_list)만 불러온다.
# 3. DB에 저장할 쿼리(query)를 입력한다.
# 4. 페이지 오류, 통신 오류 등 오류가 발생한 티커명을 저장할 리스트(error_list)를 만든다.
# 5. for문을 통해 전종목 재무제표를 다운로드 받으며, 진행상황을 알기위해 tqdm() 함수를 이용한다.
# 6. get_financials() 함수를 이용해 연간 및 분기 재무제표를 받은 후, 두 테이블을 concat() 함수를 통해 행으로 묶어준다.
# 6. 재무제표 데이터를 DB에 저장한다.
# 7. 무한 크롤링을 방지하기 위해 한 번의 루프가 끝날 때마다 타임슬립을 적용한다.
# 8. 모든 작업이 끝나면 DB와의 연결을 종료한다.
# 
# ```{figure} image/data_global/sql_fs.png
# ---
# name: sql_fs
# ---
# 글로벌 재무제표 테이블
# ```
# 
# ```{note}
# 미국 종목들의 가치지표는 국내 재무제표 데이터를 이용해 가치지표를 계산했던 것과 동일한 방법으로 계산할 수 있으므로, 이는 생략하도록 한다.
# ```
