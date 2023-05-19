# 주가 다운로드
import yfinance as yf
price = yf.download('AAPL')
price = yf.download('AAPL', progress=False)
price = yf.download('AAPL', start = '1990-01-01', progress=False)

price = yf.download("8035.T", progress = False)

# 재무제표 다운로드
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = 'https://finance.yahoo.com/quote/AAPL/financials?p=AAPL'
driver.get(url)
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[2]/button/div/span').click()

# 처음 시도 -> 안됨
tbl = driver.find_element(By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div')
tbl.text 
# ->> 띄어쓰기 문제 떄문에 불가능 

# 행 단위로 쪼개보자!
tbl_span = tbl.find_elements(By.TAG_NAME, 'span')
tbl_span[0].text
[i.text for i in tbl_span]
# - 이런게 안보임

# 제목 부분 파싱
tbl_title = tbl.find_elements(By.CLASS_NAME, 'D\(tbhg\)')[0].find_elements(By.TAG_NAME, 'span')
tbl_title_text = [i.text for i in tbl_title]
tbl_title_text
col_num = len(tbl_title_text)

# 본문 파싱
tbl_body = tbl.find_element(By.CLASS_NAME, 'D\(tbrg\)')

# 열로
tbl_body.find_elements(By.CLASS_NAME, 'D\(tbc\)')[2].text
tbl_body_text = [i.text for i in tbl_body.find_elements(By.CLASS_NAME, 'D\(tbc\)')]
tbl_body_text

# array 이용
tbl_body_text[0::6]
tbl_body_text[1::6]

tbl_body_list = []
for i in range(col_num) :
    tbl_body_list.append(tbl_body_text[i::col_num])

fs_tbl = pd.DataFrame(tbl_body_list).transpose()
fs_tbl.columns = tbl_title_text

fs_tbl = fs_tbl.loc[:, fs_tbl.columns != 'TTM'].melt(id_vars=['Breakdown'])
fs_tbl['variable'] = pd.to_datetime(fs_tbl['variable'])
fs_tbl['value'] = fs_tbl['value'].str.replace(',', '')
fs_tbl = fs_tbl[~fs_tbl['value'].isin(['0', '-'])]
fs_tbl['value'] = fs_tbl['value'].astype('float')
fs_tbl.columns = ['account', 'date', 'value']

driver.quit()

#-----------------------------------------#

# 이미지 업로드 금지
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True

chrome_options = webdriver.ChromeOptions()
# this will disable image loading
chrome_options.add_argument('--blink-settings=imagesEnabled=false')
# or alternatively we can set direct preference:
chrome_options.add_experimental_option(
    "prefs", {"profile.managed_default_content_settings.images": 2}
)

#테이블 넣으면 함수로

def fs_clean(freq) :
    
    # 테이블
    tbl = driver.find_element(By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div')
    
    # 제목 부분    
    tbl_title = tbl.find_elements(By.CLASS_NAME, 'D\(tbhg\)')[0].find_elements(By.TAG_NAME, 'span')    
    tbl_title_text = [i.text for i in tbl_title]    
    col_num = len(tbl_title_text)
    
    # 본문 부분
    tbl_body = tbl.find_element(By.CLASS_NAME, 'D\(tbrg\)')
    tbl_body.find_elements(By.CLASS_NAME, 'D\(tbc\)')[2].text
    tbl_body_text = [i.text for i in tbl_body.find_elements(By.CLASS_NAME, 'D\(tbc\)')]    
    
    # 리스트로 변환
    tbl_body_list = []
    for i in range(col_num) :
        tbl_body_list.append(tbl_body_text[i::col_num])
        
    # 데이터프레임으로 변환
    fs_tbl = pd.DataFrame(tbl_body_list).transpose()
    fs_tbl.columns = tbl_title_text
    
    # 클렌징
    fs_tbl = fs_tbl.loc[:, fs_tbl.columns != 'TTM'].melt(id_vars=['Breakdown'])
    fs_tbl['variable'] = pd.to_datetime(fs_tbl['variable'])
    fs_tbl['value'] = fs_tbl['value'].str.replace(',', '')
    fs_tbl = fs_tbl[~fs_tbl['value'].isin(['0', '-'])]
    fs_tbl['value'] = fs_tbl['value'].astype('float')
    fs_tbl.columns = ['account', 'date', 'value']    
    fs_tbl['freq'] = freq
    
    return fs_tbl

def wait_collapse():
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[2]/button/div/span')))   
    
ticker = 'META'

# 드라이버
driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)

# Income Statement
url = f'https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}'
driver.get(url)
time.sleep(2)

# 팝업 뜰 경우 [X] 누르기
if driver.find_elements(By.XPATH, '//*[@id="myLightboxContainer"]/section'):
    driver.find_element(By.XPATH, '//*[@id="myLightboxContainer"]/section/button[2]').click()

driver.find_element(By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[2]/button/div/span').click()

## 연간 데이터
data_income_y = fs_clean('y')

## 분기 데이터
driver.find_element(By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[1]/div[2]/button/div/span').click()
time.sleep(1)
data_income_q = fs_clean('q')

# Balance Sheet
url = f'https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}'
driver.get(url)
wait_collapse()
driver.find_element(By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[2]/button/div/span').click()

## 연간 데이터
data_bs_y = fs_clean('y')

## 분기 데이터
driver.find_element(By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[1]/div[2]/button/div/span').click()
time.sleep(1)
data_bs_q = fs_clean('q')

# Cashflow
url = f'https://finance.yahoo.com/quote/{ticker}/cash-flow?p={ticker}'
driver.get(url)
wait_collapse()
driver.find_element(By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[2]/button/div/span').click()

## 연간 데이터
data_cf_y = fs_clean('y')

## 분기 데이터
driver.find_element(By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[1]/div[2]/button/div/span').click()
time.sleep(1)
data_cf_q = fs_clean('q')

data_concat = pd.concat([data_income_y, data_income_q, data_bs_y, data_bs_q, data_cf_y, data_cf_q])
