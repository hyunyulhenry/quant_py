from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from slack_sdk import WebClient
from datetime import datetime

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url='https://edition.cnn.com/markets/fear-and-greed')
idx = driver.find_element(By.CLASS_NAME, value = 'market-fng-gauge__dial-number-value').text
driver.close()
idx = int(idx)
dt = datetime.today().strftime('%Y-%m-%d')

slack_token  = 'xoxb-3201556049680-3232837627973-fvhWHIWoNkJMMdgcmNvtHaMi'
client = WebClient(token=slack_token)

client.chat_postMessage(channel='#api_test',
                        text= f'''Fear and Greed: {idx} / {dt}''')

