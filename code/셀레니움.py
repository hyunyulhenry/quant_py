# https://pythondocs.net/selenium/%EC%85%80%EB%A0%88%EB%8B%88%EC%9B%80-%ED%81%AC%EB%A1%A4%EB%9F%AC-%EA%B8%B0%EB%B3%B8-%EC%82%AC%EC%9A%A9%EB%B2%95/
# https://fenderist.tistory.com/168

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup


driver = webdriver.Chrome("C:/Users/doomoolmori/Dropbox/My Book/quant_python/chromedriver.exe")
# driver = webdriver.Chrome("C:/Users/leebi/Dropbox/My Book/quant_python/chromedriver.exe")

url = 'https://www.naver.com/'

# 페이지 접속하기
driver.get(url)

 # 페이지 정보
driver.page_source

# 버튼 누르기 (뉴스)
driver.find_element(By.LINK_TEXT , value = '뉴스').click()

# 뒤로가기
driver.back()

# 검색어 넣기
driver.find_element(By.CLASS_NAME, value = 'input_text').send_keys('퀀트 투자 포트폴리오 만들기')

# 엔터키 누르기
driver.find_element(By.CLASS_NAME, value = 'btn_submit').send_keys(Keys.ENTER)

# 클리어 하고 재삭제
driver.find_element(By.CLASS_NAME, value = 'box_window').clear()
driver.find_element(By.CLASS_NAME, value = 'box_window').send_keys('이현열 퀀트')

# 검색 버튼 클릭하기
driver.find_element(By.CLASS_NAME, value = 'bt_search').click()

# VIEW 클릭하기
driver.find_element(By.XPATH, value = '//*[@id="lnb"]/div[1]/div/ul/li[2]/a').click()

# 옵션 -> 최신순
driver.find_element(By.CLASS_NAME, value = 'option_filter').click()
driver.find_element(By.XPATH, value = '//*[@id="snb"]/div[2]/ul/li[2]/div/div/a[2]').click()

# 스크롤 내리기
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
# driver.find_element(By.TAG_NAME, value = 'body').send_keys(Keys.PAGE_DOWN)

# 스크롤 끝까지 내리기
prev_height = driver.execute_script('return document.body.scrollHeight')
print(prev_height)

while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)
    
    curr_height = driver.execute_script('return document.body.scrollHeight')
    if curr_height == prev_height:
            break
    prev_height = curr_height

# 제목 / 링크 찾기
html = BeautifulSoup(driver.page_source, 'lxml')
txt = html.find_all(class_ = 'api_txt_lines total_tit _cross_trigger')

test = txt[0]
txt_name = test.get_text()
txt_link = test['href']

for i in txt:
    print(i.get_text())
    print(i['href'])
    print("---------")

driver.quit()