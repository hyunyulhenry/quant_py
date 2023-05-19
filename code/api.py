import requests
import json
import keyring
import pandas as pd

# 키 불러오기
app_key = keyring.get_password('mock_app_key', 'Henry')
app_secret = keyring.get_password('mock_app_secret', 'Henry')


# 해시키 발급
def hashkey(datas):
  path = "uapi/hashkey"
  url = f"{url_base}/{path}"
  headers = {
    'content-Type' : 'application/json',
    'appKey' : app_key,
    'appSecret' : app_secret,
    }
  res = requests.post(url, headers=headers, data=json.dumps(datas))
  hashkey = res.json()["HASH"]

  return hashkey


# 접근토큰 발급
url_base = "https://openapivts.koreainvestment.com:29443" # 모의투자

headers = {"content-type":"application/json"}
path = "oauth2/tokenP"
body = {"grant_type":"client_credentials",
        "appkey":app_key, 
        "appsecret":app_secret}

url = f"{url_base}/{path}"

res = requests.post(url, headers=headers, data=json.dumps(body))
access_token = res.json()['access_token']

########################################

# 주식 현재가 조회
path = "uapi/domestic-stock/v1/quotations/inquire-price"
url = f"{url_base}/{path}"

headers = {"Content-Type":"application/json", 
           "authorization": f"Bearer {access_token}",
           "appKey":app_key,
           "appSecret":app_secret,
           "tr_id":"FHKST01010100"}

params = {
    "fid_cond_mrkt_div_code":"J",
    "fid_input_iscd":"005930"
}

res = requests.get(url, headers=headers, params=params)
res.json()
res.json()['output']['stck_prpr']


########################################

# 주식 매수 주문 (현금)
path = "/uapi/domestic-stock/v1/trading/order-cash"
url = f"{url_base}/{path}"

data = {
    "CANO": "50068923",
    "ACNT_PRDT_CD": "01",
    "PDNO": "005930",
    "ORD_DVSN": "01",
    "ORD_QTY": "10",
    "ORD_UNPR": "0",
}

headers = {"Content-Type":"application/json", 
          "authorization":f"Bearer {access_token}",
          "appKey":app_key,
          "appSecret":app_secret,
          "tr_id":"VTTC0802U",
          "custtype":"P",
          "hashkey":hashkey(data)}

res = requests.post(url, headers=headers, data=json.dumps(data))
res.json()


## 극단적 주문 해보기
data = {
    "CANO": "50068923",
    "ACNT_PRDT_CD": "01",
    "PDNO": "005930",
    "ORD_DVSN": "00",
    "ORD_QTY": "10",
    "ORD_UNPR": "50000",
}

headers = {"Content-Type":"application/json", 
          "authorization":f"Bearer {access_token}",
          "appKey":app_key,
          "appSecret":app_secret,
          "tr_id":"VTTC0802U",
          "custtype":"P",
          "hashkey":hashkey(data)}

res = requests.post(url, headers=headers, data=json.dumps(data))
res.json()

KRX_FWDG_ORD_ORGNO = res.json()["output"]["KRX_FWDG_ORD_ORGNO"] # 한국거래소전송주문조직번호
ODNO =  res.json()["output"]["ODNO"] # 주문번호

print(KRX_FWDG_ORD_ORGNO, ODNO)

# 정정 주문하기
path = "/uapi/domestic-stock/v1/trading/order-rvsecncl"
url = f"{url_base}/{path}"

data = {
    "CANO": "50068923",
    "ACNT_PRDT_CD": "01",
    "KRX_FWDG_ORD_ORGNO":KRX_FWDG_ORD_ORGNO,
    "ORGN_ODNO":ODNO,
    "ORD_DVSN":"03",
    "RVSE_CNCL_DVSN_CD":"01", # 정정    
    "ORD_QTY":"10",
    "ORD_UNPR":"0",
    "QTY_ALL_ORD_YN": "Y",
}

headers = {"Content-Type":"application/json", 
          "authorization":f"Bearer {access_token}",
          "appKey":app_key,
          "appSecret":app_secret,
          "tr_id":"VTTC0803U",
          "custtype":"P",
          "hashkey":hashkey(data)}

res = requests.post(url, headers=headers, data=json.dumps(data))
res.json()

## 매도
path = "/uapi/domestic-stock/v1/trading/order-cash"
url = f"{url_base}/{path}"


data = {
    "CANO": "50068923",
    "ACNT_PRDT_CD": "01",
    "PDNO": "005930",
    "ORD_DVSN": "01",
    "ORD_QTY": "10",
    "ORD_UNPR": "0",
}

headers = {"Content-Type":"application/json", 
          "authorization":f"Bearer {access_token}",
          "appKey":app_key,
          "appSecret":app_secret,
          "tr_id":"VTTC0801U",
          "custtype":"P",
          "hashkey":hashkey(data)}

res = requests.post(url, headers=headers, data=json.dumps(data))
res.json()

########################################

# 주식 잔고조회
path = "/uapi/domestic-stock/v1/trading/inquire-balance"
url = f"{url_base}/{path}"

headers = {"Content-Type":"application/json", 
           "authorization": f"Bearer {access_token}",
           "appKey":app_key,
           "appSecret":app_secret,
           "tr_id":"VTTC8434R"}

params = {
    "CANO":"50068923",
    "ACNT_PRDT_CD":"01",
    "AFHR_FLPR_YN": "N",
    "UNPR_DVSN":"01",
    "FUND_STTL_ICLD_YN":"N",
    "FNCG_AMT_AUTO_RDPT_YN":"N",
    "OFL_YN":"",
    "INQR_DVSN":"01",
    "PRCS_DVSN":"00",
    "CTX_AREA_FK100": "",
    "CTX_AREA_NK100": ""
}

res = requests.get(url, headers=headers, params=params)
res.json()
res.json()['output1']
res.json()['output2']