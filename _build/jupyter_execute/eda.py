#!/usr/bin/env python
# coding: utf-8

# # 데이터 분석 배워보기
# 
# 데이터 분석이란 데이터를 불러와 수정, 가공한 후 분석을 통해 통찰력을 얻고 답을 찾아나가는 과정이다. 
# 
# 우리가 실제 다루는 대부분의 데이터는 행과 열로 이루어진 테이블 형태이다. pandas 패키지는 1차원 배열인 시리즈(Series) 및 행과 열로 이루어진 2차원 배열인 데이터프레임(DataFrame)을 통해 데이터 분석 업무를 쉽게 처리할 수 있게 해준다. 이번 장에서는 pandas 패키지를 이용한 데이터 분석 방법에 대해 살펴보도록 하자.
# 
# ## 시리즈
# 
# 시리즈란 데이터가 순차적으로 나열된 1차원 배열이며, 구조는 {numref}`series`와 같다. 인덱스(Index)와 값(Value)은 일대일 대응 관계이며, 이는 키(key)와 값(value)이 '{key:value}' 형태로 구성된 딕셔너리와 비슷하다.
# 
# ```{figure} image/eda/series.png
# ---
# name: series
# ---
# 시리즈 구조
# ```
# 
# ### 시리즈 만들기
# 
# 시리즈는 `Series()` 함수를 통해 만들 수 있다. 먼저 딕셔너리를 이용해 시리즈를 만드는 법을 살펴보자.

# In[1]:


import pandas as pd

dict_data = {'a': 1, 'b': 2, 'c': 3}
series = pd.Series(dict_data)

print(series)


# In[2]:


type(series)


# 먼저 키가 'a', 'b', 'c', 값이 1, 2, 3인 딕셔너리를 만든 후, `Series()` 함수에 입력하면 시리즈 객체로 변환된다. 결과를 살펴보면 딕셔너리의 키는 시리즈의 인덱스로, 딕셔너리의 값들은 시리즈의 값으로 변환되었다.

# In[3]:


series.index


# In[4]:


series.values


# 시리즈 뒤에 `.index`와 `.values`를 입력하면 각각 인덱스와 값의 배열을 반환한다. 
# 
# 딕셔너리가 아닌 리스트를 통해 시리즈를 만들 수도 있다.

# In[5]:


list_data = ['a', 'b', 'c']
series_2 = pd.Series(list_data)

print(series_2)


# 만일 리스트를 통해 시리즈를 만들 경우, 인덱스는 정수형 위치 인덱스(0, 1, 2, ...)가 자동으로 지정된다. 

# In[6]:


series_3 = pd.Series(list_data, index=['index1', 'index2', 'index3'])

print(series_3)


# 리스트를 통해 시리즈를 만든 후, index 옵션에 인덱스 이름을 직접 입력하여 인덱스를 생성할 수도 있다.
# 
# ###  원소 선택하기
# 
# 시리즈도 리스트 혹은 튜플과 같이 인덱싱이나 슬라이싱를 사용해 원하는 원소를 선택할 수 있다.

# In[7]:


capital = pd.Series({'Korea': 'Seoul',
                     'Japan': 'Tokyo',
                     'China': 'Beijing',
                     'India': 'New Delhi',
                     'Taiwan': 'Taipei',
                     'Singapore': 'Singapore'
                     })

print(capital)


# 먼저 키로는 국가명, 값으로는 수도로 이루어진 시리즈를 만들었다. 이 중 한국에 해당하는 데이터를 선택하는 법은 다음과 같다.

# In[8]:


capital['Korea']


# 딕셔너리에서 키 값을 입력하면 이에 해당하는 값이 선택된 것처럼, 시리즈에서는 인덱스 이름을 입력하면 이에 해당하는 값이 선택된다.

# In[9]:


capital[['Korea', 'Taiwan']]


# 시리즈의 특징 중 하나는 한번에 여러개의 인덱스를 입력할 수 있다는 점이다. 값을 찾고 싶은 인덱스를 리스트 형태로([ ]) 입력하면 이에 해당하는 모든 원소가 선택된다.

# In[10]:


capital[0]


# 시리즈는 순서가 있기 때문에 위치를 통해서도 원하는 값을 선택할 수 있다. 위치 인덱스 0을 입력하면, 이에 해당하는 첫 번째 값인 Seoul이 선택된다.

# In[11]:


capital[[0, 3]]


# 위치 인덱스를 리스트 형태로 입력하면, 역시나 이에 해당하는 원소가 출력된다.

# In[12]:


capital[0:3]


# 리스트와 동일하게 슬라이싱 기능 역시 사용이 가능하다. `0:3`은 위치 인덱스가 0 이상 3 미만을 뜻하며 이에 해당하는 값이 선택된다.
# 
# ### 시리즈 연산하기
# 
# 시리즈는 사칙 연산이 가능하다.

# In[13]:


series_1 = pd.Series([1, 2, 3])
series_2 = pd.Series([4, 5, 6])

series_1 + series_2


# 먼저 1,2,3으로 이루어진 시리즈(series_1)와 4,5,6으로 이루어진 시리즈(series_2)를 생성한다. 그 후 두 시리즈를 더하면 각각의 인덱스가 같은 값끼리 연산이 수행된다. 즉 1+4, 2+5, 3+6의 결과인 5, 7, 9가 계산된다.

# In[14]:


series_1 * 2


# 시리즈에 숫자를 연산하면 모든 원소에 연산이 적용된다. 즉 시리즈에 2을 곱하면 모든 원소에 2가 곱해져 1\*2, 2\*2, 3\*3의 결과인 2,4,6이 계산된다. 
# 
# ## 데이터프레임
# 
# 시리즈가 1차원 배열이였다면, 데이터프레임은 2차원 배열이다. 이는 흔히 엑셀에서 사용하는 행과 열로 이루어진 테이블 형태이다. 데이터프레임의 각 열은 시리즈 객체이며, 이러한 시리즈가 모여 데이터프레임을 구성한다.
# 
# ```{figure} image/eda/dataframe.png
# ---
# name: dataframe
# ---
# 데이터프레임 구조
# ```
# 
# ### 데이터프레임 만들기와 수정하기
# 
# 데이터프레임은 `DataFrame()` 함수를 통해 만들 수 있으며, 시리즈를 만드는 방법과 유사하다.

# In[15]:


dict_data = {'col1': [1, 2, 3], 'col2': [4, 5, 6], 'col3': [7, 8, 9]}
df = pd.DataFrame(dict_data)

df


# In[16]:


type(df)


# 데이터프레임을 만들기 위해서는 길이가 같은, 즉 원소의 개수가 동일한 1차원 배열이 여러개 필요한다. 이는 데이터프레임이 여러 개의 시리즈를 모아둔 것과 같기 때문이다. 먼저 키가 'col1', 'col2', 'col3'이며 각 쌍에는 값이 3개씩 들어가있는 딕셔너리를 만든다. 이를 `DataFrame()` 함수에 넣으면 딕셔너리의 키는 열이름이 되며, 딕셔너리의 값은 데이터프레임 열의 값이 된다.

# In[17]:


df2 = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

df2


# 리스트를 통해 데이터프레임을 만들수도 있다. `DataFrame()` 함수 내부에 리스트 형태인 [1, 2, 3], [4, 5, 6], [7, 8, 9]를 다시 리스트에 넣어 중첩 형태로 입력하면, 각각의 리스트가 그대로 행의 형태로 입력된다. 반면 행 인덱스와 열 이름은 기본값인 위치 인덱스가 부여된다.

# In[18]:


df3 = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                   index=['index1', 'index2', 'index3'],
                   columns=['col1', 'col2', 'col3'])

df3


# 만일 행 인덱스와 열 이름을 직접 지정하고자 할 경우, 리스트 형태로 입력하면 된다. 기존 데이터프레임의 행 인덱스와 열 이름도 변경할 수 있다.

# In[19]:


df3.index = ['행 1', '행 2', '행 3']
df3.columns = ['열 1', '열 2', '열 3']

df3


# `DataFrame.index`와 `DataFrame.columns`를 통해 각각 새로운 행 인덱스 및 열 이름을 입력하면 이에 맞게 데이터가 바뀐다.

# In[20]:


df3.rename(index={'행 1': '첫 번째 행'}, inplace=True)
df3.rename(columns={'열 1': '첫 번째 열'}, inplace=True)

df3


# 행 인덱스나 열 이름 중 원하는 부분만을 선택해 변경할 수도 있다. `DataFrame.rename(index or columns = {기존 이름:새 이름, ...})`을 입력하여 기존의 이름을 새 이름으로 변경할 수 있으며, `inplace = True` 옵션을 사용하면 원본 데이터가 변경된다.
# 
# 이번에는 데이터프레임의 행과 열을 삭제하는 방법에 대해 살펴보자.

# In[21]:


df3.drop('행 3', axis=0, inplace=True)
df3.drop('열 3', axis=1, inplace=True)

df3


# `drop()` 메서드는 행 혹은 열을 삭제한다. 삭제하고 싶은 행 인덱스 혹은 열 이름을 입력하면 해당 부분이 삭제되며, 행을 삭제할 때는 축(axis) 옵션으로 `axis = 0`을, 열을 삭제할 때는 `axis = 1`을 입력해야 한다. 마지막으로 `inplace = True` 옵션을 사용하면 원본 데이터가 변경된다.
# 
# - 행 삭제: `DataFrame.drop(행 인덱스, axis=0, inplace=True)`
# - 열 삭제: `DataFrame.drop(열 이름, axis=1, inplace=True)`
# 
# ### 열과 행 선택하기
# 
# 먼저 데이터프레임에서 열을 선택하는 법에 대해 알아보도록 하자. 열을 하나만 선택할 때는 대괄호([ ])안에 열 이름을 따옴표와 함께 입력거나, 도트(.) 다음에 열 이름을 입력하면 된다.
# 
# - `DataFrame['열 이름']`
# - `DataFrame.열 이름` (열 이름이 문자열인 경우에만 가능)
# 
# 먼저 샘플 데이터프레임을 만들어 보자.

# In[22]:


dict_data = {'col1': [1, 2, 3, 4], 'col2': [5, 6, 7, 8],
             'col3': [9, 10, 11, 12], 'col4': [13, 14, 15, 16]}
df = pd.DataFrame(dict_data, index=['index1', 'index2', 'index3', 'index4'])

df


# 이 중 첫번째 열인 'col1'을 선택하는 법은 다음과 같다.

# In[23]:


df['col1']


# In[24]:


df.col1


# In[25]:


type(df['col1'])


# `DataFrame['col1']`과  `DataFrame.col1` 모두 동일한 데이터가 선택된다. 열을 한개만 선택할 경우 시리즈 객체가 반환되며, 만일 데이터프레임 형태로 반환하고자 할 경우에는 2중 대괄호([[열 이름]]) 형태로 입력하면 된다.

# In[26]:


df[['col1']]


# In[27]:


type(df[['col1']])


# 이번에는 데이터프레임에서 2개 이상의 열을 추출하는 법에 대해 알아보자. 대괄호([ ]) 안에 열 이름을 리스트 형태로 입력하면 이에 해당하는 열들이 데이터프레임으로 반환된다. 
# 
# - `DataFrame[['열 이름 1', '열 이름 2', ..., '열 이름 n']]`
# 
# 위 예제에서 col1과 col2 열을 선택해보도록 하자.

# In[28]:


df[['col1', 'col2']]


# 이번에는 원하는 행을 선택하는 법에 대해 알아보자. 파이썬에서는 행 데이터를 선택할 때 `loc`과 `iloc` 인덱서를 사용한다. `loc`은 인덱스 이름을 기준으로 행을 선택할 때, `iloc`은 위치 인덱스를 기준으로 행을 선택할 때 사용한다.
# 
# - `DataFrame.loc['행 인덱스']`
# - `DataFrame.iloc[위치 인덱스]`
# 
# 먼저 첫번째 행을 선택하는 법에 대해 살펴보자.

# In[29]:


df.loc['index1']


# In[30]:


df.iloc[0]


# In[31]:


type(df.loc['index1'])


# `loc` 인덱서를 사용할 경우 인덱스 이름인 'index1'을 입력하였으며, `iloc` 인덱서를 사용할 경우는 위치 인덱스인 0을 입력했다. 행을 한개만 선택할 때에도 시리즈 객체가 반환되며, 2중 대괄호([[ 열 이름]])를 사용하면 데이터프레임 형태가 반환된다.

# In[32]:


df.loc[['index1']]


# In[33]:


df.iloc[[0]]


# 인덱서를 사용할 경우 슬라이싱 기능도 사용할 수 있다. 

# In[34]:


df.loc['index1':'index3']


# In[35]:


df.iloc[0:2]


# 행 인덱스 'index1'의 위치 인덱스는 0, 'index3'의 위치 인덱스는 2임에도 불구하고 `loc`과 `iloc`의 결과가 다르다. 이는 `loc`의 경우 범위의 끝을 포함하는 반면, `iloc`의 경우 범위의 끝을 제외하기 때문이다. 이를 정리하면 다음과 같다.
# 
# ```{table} 인덱서의 비교
# :name: indexor
# | 구분 | `loc` | `iloc` |
# | --- | --- | --- |
# | 대상 | 인덱스 이름 | 위치 인덱스 |
# | 범위 | 범위의 끝 포함 | 범위의 끝 제외 |
# ```
# 
# 마지막으로 행과 열을 동시에 입력하여 원하는 원소를 선택하는 법을 살펴보도록 하자. 각 인덱서를 사용하는 법의 차이는 다음과 같다.
# 
# - `DataFrame.loc['행 인덱스', '열 이름']`
# - `DataFrame.iloc[행 위치, 열 위치]`
# 
# 먼저 `loc` 인덱서를 사용한 방법을 살펴보자.

# In[36]:


df.loc['index1', 'col1']


# `loc` 인덱서를 통해 행 인덱스가 'index1', 열 이름이 'col1'인 원소가 선택되었다. 하나가 아닌 여러 원소를 선택하는 것도 가능하다.

# In[37]:


df.loc[['index1', 'index3'], ['col1', 'col4']]


# 리스트 형태로 원하는 행 인덱스 및 열 이름들을 입력하면, 해당 부분의 데이터만 선택하여 출력된다. 즉 행 인덱스가 'index1'과 'index3'인 행에서 열 이름이 'col1'과 'col4'인 열이 선택된다.
# 
# 슬라이싱을 이용해서도 원소를 선택할 수 있다.

# In[38]:


df.loc['index1':'index2', 'col1':'col3']


# 행 인덱스가 'index1'부터 'index2'까지의 행이, 열 이름이 'col1'부터 'col3' 까지의 열이 선택되었다.
# 
# `iloc` 인덱서를 사용한 방법도 살펴보자.

# In[39]:


df.iloc[0, 0]


# `iloc` 인덱서를 통해 첫 번째 행, 첫 번째 열의 원소가 선택되었다.

# In[40]:


df.iloc[[0, 2], [0, 3]]


# 각 행과 열의 위치를 리스트 형태로 넣으면 해당 부분의 원소가 선택된다.

# In[41]:


df.iloc[0:2, 0:3]


# 슬라이싱 기법으로도 원소를 선택할 수 있으며, `loc` 인덱서의 경우 범위의 끝이 포함되지만 `iloc` 인덱서는 범위의 끝이 포함되지 않는다.
# 
# ## 데이터 불러오기 및 저장하기
# 
# 데이터 분석에서 가장 첫 단계는 외부에 저장된 데이터를 프로그램으로 불러오는 일이다. 데이터가 없다면 분석도 할 수 없기 때문이다. pandas의 함수를 사용하면 다양한 형태의 파일을 불러와 데이터프레임으로 변환할 수 있으며, 반대로 가공한 데이터프레임을 다양한 유형의 파일로 저장할 수도 있다.
# 
# ```{table} 판다스의 데이터 입출력 함수
# :name: read_data
# | 파일 포맷 | 불러오기 | 저장하기 |
# | --- | --- | --- |
# | CSV | `read_csv()` | `to_csv()` |
# | EXCEL | `read_excel()` | `to_excel()` |
# | SQL | `read_sql()` | `to_sql()` |
# | HTML | `read_html()` | `to_html()` |
# | JSON | `read_json()` | `to_json()` |
# | HDF5 | `read_hdf()` | `to_hdf()` |
# ```
# 
# 이 중 가장 대표적인 파일 포맷인 CSV와 EXCEL 파일을 읽고 쓰는 법에 대해 살펴보기로 하자.

# In[42]:


import pandas as pd

data_csv = pd.read_csv(
    'https://raw.githubusercontent.com/hyunyulhenry/quant_py/main/kospi.csv')
data_csv


# `read_csv()` 함수 내에 파일 경로(파일명)을 입력하면 CSV 파일을 불러온 후 데이터프레임으로 변환한다. 파일 경로는 PC에서의 파일 위치(예: C:\Users\leebi\quant\kospi.csv) 혹은 인터넷 주소를 입력하면 된다. 해당 함수는 다양한 인자를 제공하므로 원하는 형식에 맞춰 데이터를 불러오는 것이 가능하다. 이와 관련된 자세한 설명은 아래 페이지에 설명되어 있다.
# 
# ```
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
# ```
# 
# 데이터를 불러온 것과 반대로 파이썬의 데이터프레임을 CSV 파일로 저장할때는 `to_csv()` 메서드가 사용된다.

# In[ ]:


data_csv.to_csv('data.csv')


# ```{figure} image/eda/save_csv.png
# ---
# name: save_csv
# ---
# ```
# 
# `DataFrame.to_csv('파일이름.csv')`을 입력하면 해당 경로에 CSV 파일이 저장된다. 
# 
# 이번에는 엑셀 파일을 불러오는 법을 살펴보도록 하자. 

# In[43]:


data_excel = pd.read_excel(
    'https://github.com/hyunyulhenry/quant_py/raw/main/kospi.xlsx', sheet_name='kospi')
data_excel


# `read_excel()` 함수의 사용법은 앞서 살펴본 `read_csv()` 함수의 사용법과 거의 동일한다. 함수 내에 파일 경로(파일명)을 입력하면 엑셀 파일을 불러온 후 데이터프레임으로 변환한다. 시트명을 입력하지 않으면 가장 첫 번째 시트의 데이터를 불러오며, `sheet_name`을 통해 불러오고자 하는 시트를 선택할 수도 있다.
# 
# 데이트프레임을 엑셀 파일로 저장할때는 `to_excel()` 메서드가 사용된다.

# In[ ]:


data_excel.to_excel('data.xlsx')


# ```{figure} image/eda/save_excel.png
# ---
# name: save_excel
# ---
# ```
# 
# `DataFrame.to_excel('파일이름.xlsx')`을 입력하면 해당 경로에 엑셀 파일이 저장된다. 
# 
# ## 데이터 요약 정보 및 통계값 살펴보기
# 
# 데이터를 불러왔다면 대략적인 정보를 확인하여 제대로된 데이터가 들어왔는지, 데이터는 어떠한 특성을 가지고 있는지 살펴보아야 제대로 된 데이터 분석을 할 수 있다. 먼저 데이터의 맨 위와 아래 중 일부를 확인하여 데이터를 개략적으로 살펴보는데는 `head()`와 `tail()` 메서드가 사용된다.
# 
# - 맨 위 살펴보기: `DataFrae.head(n)`
# - 맨 아래 살펴보기: `DataFrae.tail(n)`
# 
# n에 정수를 입력하면 맨 위 혹은 아래의 n개 행을 보여주며, 값을 입력하지 않으면 기본값인 5개 행을 보여준다. 예제로써 seaborn 패키지의 타이타닉 데이터셋을 불러온 후 살펴보자.

# In[44]:


import seaborn as sns

df = sns.load_dataset('titanic')
df.head()


# In[45]:


df.tail()


# 맨 위와 아래의 5개 행을 통해 데이터를 간략하게 볼 수 있다. 각 열의 데이터가 의미하는 바는 다음과 같다.
# 
# ```{table} 타이타닉 데이터셋
# :name: titanic_dataset
# | 열 이름 | 의미	| 값 |
# | --- | --- | --- |
# | survived | 생존여부 |	0 (사망) / 1 (생존)	|
# | pclass | 좌석등급 (숫자) | 1 / 2 / 3 |
# | sex | 성별	| male/female |
# | age | 나이 | 0~80 |
# | sibsp	| 형제자매 + 배우자 동승자수 | 0~8 |
# | parch | 부모 + 자식 동승자수 | 0~6 |
# | fare | 요금 | 0~512.3292 |
# | embarked | 탑승 항구 | S (Southampton), C (Cherbourg), Q (Queenstown) |
# | class | 좌석등급 (영문) | First, Second, Third |
# | who | 성별 | man / woman | True(성인 남성), False(성인 남성이 아님) |
# | adult_male | 성인 남성 인지 아닌지 여부
# | deck | 선실 고유 번호 가장 앞자리 알파벳 | A,B,C,D,E,F,G |
# | embark_town | 탑승 항구 (영문) | Southampton / Cherbourg / Queenstown |
# | alive | 생존여부 | no(사망) / yes(생존) |
# | alone | 가족 있는지 여부 |	True (가족 X) / False (가족 O) |
# ```
# 
# 이번에는 데이터프레임의 크기를 확인해보도록 하자. 

# In[46]:


df.shape


# `dataframe.shape`를 입력하면 데이터프레임의 행과 열 갯수를 튜플 형태로 반환한다. 타이타닉 데이터셋은 행이 891개, 열이 15개로 이루어져 있다. 
# 
# 데이터프레임의 기본 정보는 `info()` 메서드를 통해 확인할 수 있다.

# In[47]:


df.info()


# 1. 데이터프레임의 클래스 유형인 <'pandas.core.frame.DataFrame'>가 표시된다.
# 2. RangeIndex를 통해 행이 0부터 890까지, 총 891개가 있음이 표시된다.
# 3. Data columns를 통해 총 15개 열이 있음이 표시된다.
# 4. #은 열 번호, Column는 열 이름, Non-Null Count은 Null값이 아닌 데이터 갯수, Dtype은 데이터 형태다.
# 5. dtypes에는 데이터 형태가 요약되어 있다.
# 6. memory usage에는 메모리 사용량이 표시된다.
# 
# ```{notice}
# pandas는 넘파이(NumPy)를 기반으로 만들어진 패키지이므로 NumPy에서 사용하는 자료형을 사용한다. 이는 파이썬 기본 자료형과 비슷하지만 다소 차이가 있다.
# 
# | 파이썬 기본 자료형 | pandas 자료형 | 설명 |
# | --- | --- | --- |
# | int | int64 | 정수형 |
# | float | float64 | 실수형 |
# | string | object | 문자열 |
# | 없음, datetime 패키지 이용 | datetime64, timedelta64 | 시간 |
# | bool | bool | 불리언 |
# ```
# 
# 각 열의 고유값 개수를 구하는데는 `value_counts()` 메서드가 사용된다. 먼저 sex(성별)의 고유값의 종류와 개수를 확인해보도록 하자.

# In[48]:


df['sex'].value_counts()


# 원하는 열을 선택한 후 `value_counts()` 메서드를 적용한다. 고유값에는 male과 female이 있으며 male 데이터는 577개, female 데이터는 314개가 있다. 하나가 아닌 다중 열을 기준으로도 해당 메서드를 적용할 수 있다.

# In[49]:


df[['sex', 'survived']].value_counts()


# sex와 survived 열을 기준으로 고유값 별 갯수가 계산되었다. male/0(남성/사망)은 468개, female/1(여성/생존)은 233개, male/1(남성/생존)은 109개, female/0(여성/사망)은 81개 데이터가 있다. 그러나 정렬이 보기 불편한 형태이며, 개수가 아닌 비중으로 보는게 편할 수도 있다. 이번에는 이를 반영해보도록 하자.

# In[50]:


df[['sex', 'survived']].value_counts(normalize=True).sort_index()


# `value_counts()` 내에 `normalize=True`를 입력하면 비중으로 계산된다. 즉 female/0은 전체 891개 데이터 중 81개 이므로 81/891 = 0.090909가 계산된다. 또한 `sort_index()` 메서드는 인덱스를 정렬해준다.
# 
# pandas의 메서드를 이용하면 각종 통계값도 쉽게 구할 수 있다. 가장 많이 사용되는 통계값인 산술평균은 `mean()` 메서드를 통해 구할 수 있다.

# In[51]:


df['survived'].mean()


# 원하는 열을 선택한 후, `mean()`을 입력하면 평균이 계산된다. survived에서 0은 사망, 1은 생존을 의미하므로 평균인 0.38은 전체 사람 중 38%의 사람이 생존했다는 의미와 같다.

# In[52]:


df[['survived', 'age']].mean()


# 여러개의 열을 리스트 형태로 입력하여 동시에 평균을 구할 수도 있다. 타이타닉호 탑승자의 평균연령은 약 30세 였다. 
# 
# 그러나 극단적인 값이 존재할 경우 산술평균은 왜곡될 수 있다. fare(요금) 열의 특성을 살펴보자.

# In[53]:


df['fare'].min()


# In[54]:


df['fare'].max()


# In[55]:


df['fare'].mean()


# `min()`과 `max()` 메서드는 각각 최소값과 최대값을 계산한다. 요금의 최저는 0원도 있는 반면, 최대는 512나 된다. 따라서 평균인 32는 극단치에 해당하는 비싼 요금들의 영향을 받았을 가능성이 높다. 이러한 경우 중위수를 의미하는 median이 더욱 평균을 잘 설명해준다고 볼 수 있으며, 이는 `median()` 메서드를 통해 계산이 가능하다.

# In[56]:


df['fare'].median()


# fare 열의 중위수는 14로써 산술평균인 32보다 훨씬 낮다. 이처럼 데이터가 극단치가 있는 경우 산술평균과 함께 중위수를 확인할 필요가 있다.
# 
# pandas 패키지에는 이 외에도 통계값을 계산할 수 있는 다양한 메서드가 존재한다.
# 
# ## 결측치 처리하기
# 
# 타이타닉 데이터셋을 살펴보면 NaN이라는 데이터가 있다.

# In[57]:


df.head()


# NaN은 'Not a Number'의 약자로써 결측치 혹은 누락값이라고 하며, 데이터를 입력할 때 빠지거나 소실된 값이다. 결측치가 많아지면 데이터의 품질이 떨어지고 제대로된 분석을 할 수 없기 때문에 적절하게 처리하는 과정이 필요하다. 먼저 결측치의 독특한 특성에 대해 살펴보자. 앞선 예제에서 `info()` 메서드를 통해 non-null인 데이터의 갯수, 즉 결측치가 아닌 데이터의 갯수를 확인할 수 있었다.

# In[58]:


df.info()


# deck 열에는 값이 203개 밖에 없으며, 891-203 = 688개 만큼의 결측치가 있음을 확인할 수 있다. 결측치를 찾는 방법으로는 `isnull()`과 `notnull()` 메서드가 있다.
# 
# - `isnull()`: 결측치면 True, 유효한 데이터면 False를 반환한다.
# - `notnull()`: 유효한 데이터면 True, 결측치면 False를 반환한다.
# 
# 타이타닉 데이터셋의 맨 위 데이터에 해당 메서드를 적용해보자.

# In[59]:


df.head().isnull()


# 앞서 1, 3, 5행의 deck 열은 결측치였으며, `isnull()` 메서드를 적용하면 해당 부분이 True로 나타난다.
# 
# ### 결측치 삭제하기
# 
# 결측치를 다루는 가장 간단한 방법은 결측치가 있는 행 또는 열을 삭제하는 것이며, `dropna()` 메서드를 사용한다.

# In[60]:


df.dropna()


# `dropna()` 메서드는 데이터가 결측치가 있을 경우 해당 행을 모두 삭제한다. 891개 행이던 데이터가 182개로 줄어든 것이 확인된다. 

# In[61]:


df.dropna(subset = ['age'], axis = 0)


# `dropna()` 메서드 내에 `subset`을 입력하면 해당 열 중에서 결측치가 있는 경우 행을 삭제한다. 참고로 `axis = 0`은 행 방향으로 동작하는 것을 의미한다..
# 
# 이번에는 결측치가 있는 열을 삭제해보도록 하겠다.

# In[62]:


df.dropna(axis = 1)


# `axis = 1`을 입력하면 열 방향을 동작하여 결측치가 있는 열을 삭제한다. 즉 15개의 열 중 결측치가 존재하는 age, embarked, deck, embark_town 4개 열이 삭제되어 11개 열만 남게된다. 그러나 deck 열을 제외한 나머지 3개 열은 결측치가 얼마 없음에도 불구하고 일괄적으로 삭제되었다. 이러한 경우 기준치를 추가할 수 있다.

# In[63]:


df.dropna(axis=1, thresh=300)


# `thresh = 300`는 결측치가 300개 이상 갖는 열을 삭제한다는 의미며, deck 열만 이 조건에 부합하여 삭제되었다.
# 
# ### 결측치 대체하기
# 
# 결측치가 있는 경우 데이터를 삭제해버리면 데이터의 양이 줄어들거나 편향되어 제대로 된 분석을 할 수 없을수도 있다. 따라서 데이터에 결측이 있을 경우 다른 값으로 대체하는 방법을 쓰기도 한다. 먼저 가장 간단한 방법은 특정 값으로 변경하는 것이며, 대표적으로 결측치를 평균으로 변경한다. 예를 들어 'age' 열의 결측치는 나머지 승객의 평균나이로 대체해보도록 하자.

# In[64]:


df_2 = df.copy()

df_2.head(6)


# 먼저 데이터프레임을 복사한 후 데이터를 살펴보면, 6번째 행의 age가 NaN으로 나타난다.

# In[65]:


mean_age = df_2['age'].mean()
print(mean_age)


# 'age' 열의 평균을 구하면 대략 30세가 나온다. 이제 결측치를 해당 값으로 변경하며, 결측치를 특정 값으로 대체할 때는 `fillna()` 메서드를 사용하면 된다.

# In[66]:


df_2['age'].fillna(mean_age, inplace=True)


# `fillna()` 내에 인자를 입력하면 결측치를 해당 값으로 대체한다. 또한 `inplace = True`를 입력하면 원본 객체를 변경한다.

# In[67]:


df_2['age'].head(6)


# 다시 데이터를 확인해보면 NaN 였던 6번째 행이 평균값인 29.699로 바뀌었다. 
# 
# `fillna()`를 통해 숫자가 아닌 문자로 변경할 수도 있다. embark_town의 결측치는 가장 데이터가 많은 'Southampton'으로 바꾸도록 하자.

# In[68]:


df_2['embark_town'].fillna('Southampton', inplace=True)


# 또한 서로 이웃하고 있는 데이터끼리는 유사성을 가질 가능성이 높으며, 특히 시계열 데이터는 더욱 그러하다. 이 경우 결측치를 바로 앞이나 뒤의 값으로 변경하는 것이 좋다. 먼저 결측치를 직전 행의 값으로 바꿔주는 예를 살펴보자.

# In[69]:


df_2['deck_ffill'] = df_2['deck'].fillna(method='ffill')
df_2['deck_bfill'] = df_2['deck'].fillna(method='bfill')

df_2[['deck', 'deck_ffill', 'deck_bfill']].head(12)


# `fillna()` 메서드에 `method = 'ffill'`을 입력하면 결측치가 있는 경우 위의 행 중 결측치가 나타나기 전의 값으로 바꿔주며 'deck_ffill' 열을 통해 이를 확인할 수 있다. 1행의 경우 처음부터 결측치이므로 참조할 값이 없어 그대로 결측치로 남아있다.
# 
# 반면 `method = 'bfill'`을 입력하면 결측치가 있는 아래의 행 중 결측치가 아닌 첫 번째 값으로 바꿔주며, 'deck_bfill' 열을 통해 이를 확인할 수 있다.
# 
# ## 인덱스 다루기
# 
# 데이터프레임의 인덱스를 변경하거나 정렬하고, 재설정하는 법에 대해 살펴보도록 하자. 예제로써 seaborn 패키지의 mpg 데이터셋을 사용한다.

# In[70]:


import seaborn as sns

df = sns.load_dataset('mpg')
df.head()


# 인덱스를 확인해보면 [0, 1, 2, .. ]로 위치 인덱스의 형태로 입력되어 있다. 이처럼 데이터를 불러오면 일반적으로 위치 인덱스가 입력된다. 먼저 인덱스를 자동차 이름인 'name' 열을 인덱스로 설정하도록 하자. 인덱스 설정에는 `set_index()` 메서드가 사용된다.

# In[71]:


df.set_index('name', inplace=True)
df.head()


# `set_index()` 내에 인덱스로 설정하고자 하는 열을 입력하면 해당 열이 인덱스로 변경되며, `inplace = True`를 입력하면 원본 객체를 변경한다. 결과를 살펴보면 기존 'name' 열의 데이터가 인덱스로 변경되어 행 인덱스 형태가 되었다.
# 
# 이번에는 인덱스를 순서대로 정렬해보도록 하겠다. 인덱스 정렬에는 `sort_index()` 메서드가 사용된다.

# In[72]:


df.sort_index(inplace=True)
df.head()


# `sort_index()` 메서드를 통해 인덱스가 알파벳 순서대로 정렬되며, 기본값인 오름차순(A→Z)으로 정렬된다.

# In[73]:


df.sort_index(inplace=True, ascending=False)
df.head()


# 내림차순(Z→A) 순서로 정렬하고 싶을 경우 `ascending = False`를 입력해준다.
# 
# 마지막으로 인덱스 재설정에는 `reset_index()` 메서드를 사용한다.

# In[74]:


df.reset_index(inplace=True)
df.head()


# `reset_index()` 메서드를 사용하면 인덱스가 다시 [0, 1, 2..]의 위치 인덱스로 변경되며, 기존에 존재하던 인덱스는 'name' 열로 옮겨진다.
# 
# ## 필터링
# 
# 필터링이란 시리즈 혹은 데이터프레임의 데이터에서 조건을 만족하는 원소만 추출하는 것으로써, 엑셀의 필터와 비슷한 개념이다. 필터링에는 크게 불리언 인덱싱(boolean indexing)과 `isin()` 메서드가 사용된다. 
# 
# ### 불리언 인덱싱
# 
# 먼저 불리언 인덱싱에 대해 알아보자. 시리즈 객체에 조건을 입력하면 각 원소에 대해 참 혹은 거짓을 판별하여 True/False로 이루어진 시리즈가 반환된다. 그 후 참에 해당하는 데이터만 선택하면 결과적으로 조건을 만족하는 데이터만 추출할 수 있다. mpg 데이터셋을 다시 불러오도록 하자.

# In[75]:


df = sns.load_dataset('mpg')
df.tail(10)


# 'cylinders' 열은 자동차의 실린더 개수를 의미하며, 어떠한 값이 있는지 확인해보자.

# In[76]:


df['cylinders'].unique()


# `unique()` 메서드는 고유한 값을 반환하며, [3, 4, 5, 6, 8]이 있다. 이 중 실린더가 4인 조건을 입력한다.

# In[77]:


filter_bool = (df['cylinders'] == 4)
filter_bool.tail(10)


# `df['cylinders'] == 4`는 실린더 열이 4인 조건을 의미한다. 원래의 데이터와 비교해보면 실린더가 4인 원소는 True가, 그렇지 않으면 False가 반환되었다. 이제 해당 불리언 시리즈를 데이터프레임에 대입해보도록 한다.

# In[78]:


df.loc[filter_bool, ]


# 행 인덱스에 불리언 시리즈를 입력하면 해당 조건을 만족하는 행만 선택되며, 총 398개 행 중 204개만 남게 되었다.
# 
# 조건을 하나가 아닌 여러개를 입력할 수도 있다. 이번에는 실린더 개수가 4개이고, 마력이 100 인상인 데이터를 선택해보도록 한다.

# In[79]:


filter_bool_2 = (df['cylinders'] == 4) & (df['horsepower'] >= 100)
df.loc[filter_bool_2, ['cylinders', 'horsepower', 'name']]


# `&` 연산자를 통해 원하는 조건들을 결합하면 두개 조건을 동시에 만족하는 데이터가 선택되었다. 또한 열 이름을 리스트 형태로 입력하면 해당 열만 선택된다. 
# 
# ### `isin()` 메서드
# 
# 만일 name이 'ford maverick', 'ford mustang ii', 'chevrolet impala'인 데이터를 선택하려면 어떻게 해야할까? 불리언 인덱싱을 사용하면 다음과 같이 입력해야 한다.

# In[80]:


filter_bool_3 = (df['name'] == 'ford maverick') | (
    df['name'] == 'fford mustang ii') | (df['name'] == 'chevrolet impala')
df.loc[filter_bool_3, ]


# 각각의 조건을 or 조건에 해당하는 `|` 연산자를 통해 결합하면 세 개 조건 중 하나를 만족하는 데이터가 선택된다. 그러나 이러한 방법은 코드가 너무 길어지며, `df['name']`가 계속해서 반복된다. `isin()` 메서드를 이용하면 특정 값을 가진 행을 추출할 수 있으며, 동일한 결과를 훨씬 간단하게 나타낼 수 있다.

# In[81]:


filter_isin = df['name'].isin(
    ['ford maverick', 'ford mustang ii', 'chevrolet impala'])
df.loc[filter_isin, ]


# `isin()` 메서드 내에 조건들을 리스트 형태로 입력하면, 해당 값이 존재하는 행은 True를, 값이 없으면 False를 반환한다. 결과를 확인해보면 위의 불리언 인덱싱을 사용한 방법과 값이 동일하다.
# 
# 마지막으로 선택된 조건을 horsepower 순으로 정렬해보도록 하자.

# In[82]:


df.loc[filter_isin, ].sort_values('horsepower')


# `sort_values()` 메서드는 입력한 열의 값 기준으로 정렬을 해준다. horsepower가 낮은 것부터 오름차순으로 정렬이 되며, 내림차순으로 정렬하고자 하면 `ascending=False`을 입력하면 된다.
# 
# ## 새로운 열 만들기
# 
# 기존에 존재하는 데이터를 바탕으로 새로운 열을 만드는 법에 대해 알아보겠다. mpg 데이터셋에서 mpg 열은 연비, wt 열은 무게를 나타내며, 무게 대비 연비(mpg/wt)를 나타내는 'ratio' 열을 만들어보도록 하자.

# In[83]:


df['ratio'] = (df['mpg'] / df['weight']) * 100
df.head()


# 시리즈끼리는 서로 연산이 가능하므로, mpg 열을 weight 열로 나눈 후 100을 곱한다. 그 후 데이터프레임에 `[ ]`를 붙여 새롭게 만들 열 이름을 입력하고 계산한 결과를 입력한다. 결과를 확인해보면 가장 오른쪽에 'ratio' 열이 새롭게 만들어진다.
# 
# 특정 열의 조건을 기반으로 새로운 열을 만들 수 있으며, 이 경우 조건문 함수가 사용된다. 조건문 함수는 특정 조건을 만족했는지 여부에 따라 서로 다른 값을 부여하며, 대표적으로 NumPy 패키지의 `where()` 함수가 사용된다. 아래의 예를 살펴보자.

# In[84]:


import numpy as np

num = pd.Series([-2, -1, 1, 2])
np.where(num >= 0)


# 먼저 -2부터 2까지 숫자로 이루어진 시리즈(num)를 만들었다, 그 후 `where()` 함수 내에 조건을 입력하면 조건이 True인 지점의 인덱스를 반환한다.

# In[85]:


np.where(num >= 0, '양수', '음수')


# 조건 뒤의 두 번째와 세 번째 인자에 값을 추가하면 조건을 만족하는 부분은 두 번째 인자(양수)를, 그렇지 않은 부분은 세 번째 인자(음수)를 부여한다. 이는 엑셀에서의 `if` 함수와 같다. 이를 응용하여 horsepower가 100 미만, 100 이상, 200 이상인지를 구분하는 열을 만들어보도록 하자.

# In[86]:


import numpy as np

df['horse_power_div'] = np.where(
    df['horsepower'] < 100, '100 미만',
    np.where((df['horsepower'] >= 100) & (df['horsepower'] < 200), '100 이상',
             np.where(df['horsepower'] >= 200, '200 이상', '기타')))

df.head(8)


# 먼저 `where()` 함수 내에 horsepower가 100 보다 작을 경우 '100 미만'이라고 입력한다. 그렇지 않을 경우에는 다시 `where()` 함수를 사용하여 horsepower가 100 이상이고 200 미만일 경우에는 '100 이상', horsepower가 200 보다 클 경우에는 '200 이상', 마지막으로 모든 조건을 만족하지 않으면 '기타'를 부여한다. 그 후 해당 결과를 'horse_power_div' 열에 추가하면 'horsepower'열을 조건으로 하는 새로운 열이 만들어진다.
# 
# ## 데이터프레임 합치기
# 
# 필요한 데이터가 하나의 데이터프레임에 모두 있는 경우는 드물다. 따라서 여러 데이터프레임을 하나로 합치거나 연결해야 할 경우가 많다. pandas에서 데이터프레임을 합치는 함수에는 `concat()`, `merge()`, `join()` 이 있다.
# 
# ### `concat()` 함수
# 
# 먼저 행 혹은 열 방향을 데이터프레임을 이어 붙이는 개념인 `concat()` 함수에 대해 살펴보도록 하자.
# 

# In[ ]:


import pandas as pd

df1 = pd.DataFrame({
    "A": ["A0", "A1", "A2", "A3"],
    "B": ["B0", "B1", "B2", "B3"],
    "C": ["C0", "C1", "C2", "C3"],
    "D": ["D0", "D1", "D2", "D3"]
},
    index=[0, 1, 2, 3],
)

df2 = pd.DataFrame({
    "A": ["A4", "A5", "A6", "A7"],
    "B": ["B4", "B5", "B6", "B7"],
    "C": ["C4", "C5", "C6", "C7"],
    "D": ["D4", "D5", "D6", "D7"]
},
    index=[4, 5, 6, 7],
)

df3 = pd.DataFrame({
    "A": ["A8", "A9", "A10", "A11"],
    "B": ["B8", "B9", "B10", "B11"],
    "C": ["C8", "C9", "C10", "C11"],
    "D": ["D8", "D9", "D10", "D11"]
},
    index=[8, 9, 10, 11],
)

result = pd.concat([df1, df2, df3])

result


# ```{figure} image/eda/merging_concat_basic.png
# ---
# name: merging_concat_basic
# ---
# concat - 기본
# ```
# 
# 데이터프레임 df1, df2, df3는 열 인덱스가 A, B, C, D로 이루어져 있다. 이들을 `concat()` 함수 내에 리스트 형태로 입력하면 행 방향으로 데이터프레임이 합쳐진다. 이번에는 열 이름이 서로 다른 경우를 살펴보자. 

# In[ ]:


df4 = pd.DataFrame({
    "B": ["B2", "B3", "B6", "B7"],
    "D": ["D2", "D3", "D6", "D7"],
    "F": ["F2", "F3", "F6", "F7"]
},
    index=[2, 3, 6, 7]
)

result = pd.concat([df1, df4])

result


# ```{figure} image/eda/merging_concat_ignore_index.png
# ---
# name: merging_concat_ignore_index
# ---
# concat - 열 이름이 다른 경우
# ```
# 
# df1은 열 이름이 A, B, C, D 이지만 df4는 열 이름이 B, D, F로 구성되어 있다. 이 두개의 데이터프레임을 `concat()` 함수로 합치면 열 이름이 합집합을 기준으로 생성되며, 해당하는 열에 데이터가 없는 경우 `NaN`으로 입력된다. df1의 경우 F열이 없으므로 NaN이, df4의 경우 A, C열이 없으므로 NaN으로 채워진다.
# 
# 행 인덱스를 초기화 하고 싶을 경우 `ignore_index=True`를 입력한다.

# In[ ]:


result = pd.concat([df1, df4], ignore_index=True)

result


# ```{figure} image/eda/merging_concat_ignore_index_row.png
# ---
# name: merging_concat_ignore_index_row
# ---
# concat - 행 인덱스 초기화
# ```
# 
# 기존에는 원래 데이터프레임의 행 인덱스가 그대로 유지되었으나, `ignore_index=True`를 입력하면 행 인덱스가 초기화 되어 0에서부터 7까지의 값을 가진다.
# 
# 이번에는 행이 아닌 열 기준으로 데이터를 합쳐보도록 하자.

# In[ ]:


result = pd.concat([df1, df4], axis=1)

result


# ```{figure} image/eda/merging_concat_axis1.png
# ---
# name: merging_concat_axis1
# ---
# concat - 열 방향으로 합치기
# ```
# 
# `axis=1` 인자를 입력하면 열 방향으로 데이터가 합쳐지며, 행 인덱스를 기준으로 연결된다. df1은 행 인덱스가 0, 1, 2, 3이며 df4는 행 인덱스가 2, 3, 6, 7이다. 따라서 `concat()` 함수의 결과 행 인덱스는 합집합인 0, 1, 2, 3, 6, 7이 생성되며 해당하는 행에 데이터가 없을 경우 `NaN`으로 입력된다. 만일 합집합이 아닌 교집합을 기준으로 사용하고 싶을 경우 `join = inner` 인자를 추가로 입력한다.

# In[ ]:


result = pd.concat([df1, df4], axis=1, join="inner")

result


# ```{figure} image/eda/merging_concat_axis1_inner.png
# ---
# name: merging_concat_axis1_inner
# ---
# concat - 열 방향으로 합치기 (교집합)
# ```
# 
# 두 데이터프레임이 공통으로 존재하는 행 인덱스인 2, 3을 기준으로만 데이터가 합쳐졌다. 
# 
# 데이터프레임에 시리즈를 합칠수도 있다.

# In[ ]:


s1 = pd.Series(["X0", "X1", "X2", "X3"], name="X")
result = pd.concat([df1, s1], axis=1)

result


# ```{figure} image/eda/merging_concat_mixed_ndim.png
# ---
# name: merging_concat_mixed_ndim
# ---
# concat - 시리즈 합치기
# ```
# 
# 원래 데이터프레임의 각 열은 시리즈로 구성되어 있으므로, 기존의 데이터프레임에 시리즈를 합칠수 있다.
# 
# ### `merge()` 함수
# 
# `merge()` 함수는 기준이 되는 열이나 인덱스, 즉 키(key)를 기준으로 두 데이터프레임을 합친다. 데이터프레임을 병합하는 방법은 크게 inner join, left join, right join, outer join으로 구분된다.
# 
# 
# - inner join: `pd.merge(left, right, on = 'inner')` (on = 'inner'는 생략 가능)
# - left join: `pd.merge(left, right, on = 'left')`
# - right join: `pd.merge(left, right, on = 'right')`
# - outer join: `pd.merge(left, right, on = 'outer')`
# 
# ```{figure} image/eda/inner_join.png
# ---
# scale: 50%
# name: inner_join
# ---
# inner join
# ```
# 
# inner join은 양쪽 데이터프레임에서 기준이 되는 열의 데이터가 모두 있는 교집합 부분만 반환한다. 예를 살펴보자.

# In[ ]:


left = pd.DataFrame({
    "key": ["K0", "K1", "K2", "K3"],
    "A": ["A0", "A1", "A2", "A3"],
    "B": ["B0", "B1", "B2", "B3"]
})


right = pd.DataFrame({
    "key": ["K0", "K1", "K3", "K4"],
    "C": ["C0", "C1", "C3", "C4"],
    "D": ["D0", "D1", "D3", "D4"],
})

result = pd.merge(left, right, on="key")

result


# ```{figure} image/eda/inner_join_result.png
# ---
# name: inner_join_result
# ---
# inner join 결과
# ```
# 
# 합치려는 두 데이터프레임을 `merge()` 함수에 입력하며, 기준이 되는 열을 `on` 뒤에 입력한다. `merge()` 함수는 기본적으로 inner join으로 데이터를 합친다. left 데이터프레임에서 key 열의 값은 K0, K1, K2, K3이며, right 데이터프레임에서 key 열의 값은 K0, K1, K3, K4다. 따라서 key 열의 데이터가 둘의 교집합에 해당하는 K0, K1, K3인 행만 선택되어 열 방향으로 합쳐졌다.
# 
# ```{figure} image/eda/left_join.png
# ---
# scale: 50%
# name: left_join
# ---
# left join
# ```
# 
# left join은 왼쪽 데이터프레임은 유지가 되며, 오른쪽 데이터프레임이 키를 기준으로 합쳐진다.

# In[ ]:


result = pd.merge(left, right, on="key", how='left')

result


# ```{figure} image/eda/left_join_result.png
# ---
# name: left_join_result
# ---
# left join 결과
# ```
# 
# 먼저 left 데이터프레임은 형태를 유지하며, right 데이터프레임은 키 값을 기준으로 열 방향으로 합쳐진다. right 데이터프레임의 key 열에는 K2 값이 없으므로 해당 부분은 NaN으로 채워지며, right 데이터프레임에만 존재하는 K4 값에 해당하는 부분은 삭제된다.
# 
# ```{figure} image/eda/right_join.png
# ---
# scale: 50%
# name: right_join
# ---
# right join
# ```
# 
# right join은 left join과 반대로 오른쪽 데이터프레임이 유지가 되며, 왼쪽 데이터프레임이 키를 기준으로 합쳐진다.

# In[ ]:


result = pd.merge(left, right, on="key", how='left')

result


# ```{figure} image/eda/right_join_result.png
# ---
# name: right_join_result
# ---
# right join 결과
# ```
# 
# 이번에는 right 데이터프레임에 있는 key 값인 K0, K1, K3, K4을 기준으로 left 데이터프레임이 합쳐졌다.
# 
# ```{figure} image/eda/outer_join.png
# ---
# scale: 50%
# name: outer_join
# ---
# outer join
# ```
# 
# outer join은 데이터프레임 중 어느 한쪽에만 속하더라도 상관없이 합집합 부분을 반환한다.

# In[ ]:


result = pd.merge(left, right, on="key", how='outer')

result


# ```{figure} image/eda/outer_join_result.png
# ---
# name: outer_join_result
# ---
# outer join 결과
# ```
# 
# 두 데이터프레임의 key 열에 존재하는 모든 데이터 K0, K1, K2, K3, K4를 기준으로 데이터들이 합쳐진다.
# 
# 기준이 되는 열의 이름이 서로 다른 경우는 `left_on`과 `right_on`을 통해 키를 직접 선언한다.

# In[ ]:


left = pd.DataFrame({
    "key_left": ["K0", "K1", "K2", "K3"],
    "A": ["A0", "A1", "A2", "A3"],
    "B": ["B0", "B1", "B2", "B3"]
})


right = pd.DataFrame({
    "key_right": ["K0", "K1", "K3", "K4"],
    "C": ["C0", "C1", "C3", "C4"],
    "D": ["D0", "D1", "D3", "D4"],
})

result = pd.merge(left, right, left_on='key_left',
                  right_on='key_right', how='inner')

result


# ```{figure} image/eda/left_join_result_diff.png
# ---
# name: left_join_result_diff
# ---
# left join (키가 다른 경우)
# ```
# 
# `merge(left, right)`가 아닌 `left.merge(right)` 형태로 함수를 작성할 수도 있다.

# In[ ]:


result = left.merge(right, left_on='key_left',
                    right_on='key_right', how='inner')

result


# ```{figure} image/eda/left_join_result_diff.png
# ---
# name: left_join_result_diff
# ---
# left.merge(right) 형태
# ```
# 
# 해당 방법으로 코드를 작성할 경우 왼쪽 데이터프레임에 오른쪽 데이터프레임을 붙인다는 점이 더욱 직관적으로 표현된다.
# 
# ### `join()` 메서드
# 
# `join()` 메서드는 `merge()` 함수를 기반으로 만들어져 사용방법이 거의 비슷하다. 다만, `join()` 메서드는 두 데이터프레임의 행 인덱스를 기준으로 데이터를 결합한다.

# In[ ]:


left = pd.DataFrame({
    "A": ["A0", "A1", "A2", "A3"],
    "B": ["B0", "B1", "B2", "B3"]},
    index=["K0", "K1", "K2", "K3"]
)


right = pd.DataFrame({
    "C": ["C0", "C1", "C3", "C4"],
    "D": ["D0", "D1", "D3", "D4"]},
    index=["K0", "K1", "K3", "K4"])

result = left.join(right)

result


# ```{figure} image/eda/join.png
# ---
# name: join
# ---
# join 함수
# ```
# 
# `join()` 메서드는 디폴트로 left join 방법을 사용한다. `merge()` 함수는 키를 기준으로 결합을, `join()` 메서드는 행 인덱스를 기준으로 결합을 한다는 점을 제외하고 나머지 사용법은 거의 비슷하다.
# 
# ## 데이터 재구조화
# 
# 데이터프레임의 행과 열 구조를 변형하거나, 특정 요인에 따라 집계를 하는 방법에 대해 알아보겠다. pandas에서 데이터 재구조화에 사용되는 함수는 `melt()`, `pivot_table()`, `stack()`, `unstack()` 등이 있다. 예제로써 seaborn 패키지의 팽귄 데이터를 사용한다.

# In[87]:


import seaborn as sns

df = sns.load_dataset('penguins')
df.head()


# 해당 데이터는 팔머(Palmer) 펭귄의 세가지 종에 대한 데이터이며, 각 열의 내용은 다음과 같다.
# 
# - species: 펭귄 종으로써 아델리(Adelie), 젠투(Gentoo), 턱끈(Chinstrap) 펭귄 세가지 종이 있다.
# - island: 남극의 펭귄 서식지로써 Torgersen, Biscoe, Dream가 있다.
# - bill_length_mm: 부리의 길이에 해당한다.
# - bill_depth_mm: 부리의 위아래 두께에 해당한다.
# - flipper_length_mm: 펭귄의 날개에 해당한다.
# - body_mass_g: 몸무게에 해당한다.
# - sex: 성별에 해당한다.
# 
# #### `melt()`
# 
# `melt()` 함수는 ID 변수를 기준으로 원본 데이터프레임의 열 이름들을 variable 열에, 각 열에 있던 데이터는 value 열에 넣어 아래로 긴 형태로 만들어준다.

# In[88]:


df.melt(id_vars=['species', 'island']).head(10)


# `id_vars`에 입력한 열은 식별자 변수에 해당하므로 원래의 열이 그대로 유지된다. 반면 그 외의 열 이름인 bill_length_mm,	bill_depth_mm, flipper_length_mm, body_mass_g, sex가 variable 열에 입력되며, 각 열의 데이터가 value 열에 매칭된다.
# 
# ### `pivot_table()`
# 
# `pivot_table()` 함수는 엑셀의 피벗 테이블과 비슷하며 총 4개 입력값이 필요하다.
# 
# - index: 행 인덱스
# - columns: 열 인덱스
# - values: 데이터 값
# - aggfunc: 데이터 집계 함수
# 
# 펭귄 데이터의 species와 island 별로 bill_length_mm의 평균을 구해보자.

# In[89]:


df_pivot_1 = df.pivot_table(index='species',
                            columns='island',
                            values='bill_length_mm',
                            aggfunc='mean')

df_pivot_1


# 행 인덱스에는 species, 열 인덱스에는 island, 데이터 값에는 bill_length_mm, 집계 함수는 mean을 입력하면 테이블 형태의 결과를 반환한다. Chinstrap-Biscoe, Chinstrap-Torgersen, Gentoo-Dream, Gentoo-Torgersen 처럼 데이터가 없는 값은 NaN으로 채워진다.
# 
# 각 인덱스를 하나가 아닌 여러개를 입력할 수 있으며, 데이터 값, 집계 함수 역시 여러개를 입력할 수 있다.

# In[90]:


df_pivot_2 = df.pivot_table(index=['species', 'sex'],
                            columns='island',
                            values=['bill_length_mm', 'flipper_length_mm'],
                            aggfunc=['mean', 'count'])

df_pivot_2


# 행으로는 species와 sex, 열로는 island, 데이터 값에는 bill_length_mm와 flipper_length_mm을 입력했으며, 집계 함수로 입력한 평균 및 갯수가 계산되었다. 이처럼 복수의 조건을 입력하고 싶을 경우는 리스트 형태로 입력하면 된다.
# 
# ### `stack()`과 `unstack()`
# 
# `stack()` 메서드와 `unstack()` 메서드는 열 인덱스를 행 인덱스로 바꾸거나 반대로 행 인덱스를 열 인덱스로 변경한다.
# 
# - `stack()`: 열 인덱스를 행 인덱스로 변환
# - `unstack()`: 행 인덱스를 열 인덱스로 변환
# 
# 먼저 `pivot_table()`을 통해 아래의 데이터프레임을 만들자.

# In[91]:


df_pivot_4 = df.pivot_table(index=['species', 'sex'],
                            columns='island',
                            values='bill_length_mm',
                            aggfunc='mean')

df_pivot_4


# 위 데이터프레임에 `stack()` 메서드를 적용해보자.

# In[92]:


df_pivot_4.stack()


# 열 인덱스인 Biscoe, Dream, Torgersen이 행 인덱스로 변경되었다. 해당 결과물은 시리즈 형태이며, 데이터프레임으로 변경하고 싶을 경우 `to_frame()` 메서드를 추가한다.

# In[93]:


df_pivot_4.stack().to_frame()


# 이번에는 `unstack()` 메서드를 적용해보도록 하자.

# In[94]:


df_pivot_4.unstack()


# 행 인덱스인 Female, Male이 열 인덱스로 변경되었다.
# 
# ## 데이터프레임에 함수 적용하기
# 
# `apply()` 메서드를 사용하면 시리즈나 데이터프레임의 개별 원소에 함수를 적용할 수 있다. 이는 사용자가 직접 만든 함수(lambda 함수 포함)를 적용할 수 있어 기본함수로 처리하기 어려운 복잡한 연산도 가능하며, for문을 사용해 각 데이터에 함수를 적용하는 것 보다 더 빠르게 연산이 가능하다.
# 
# ### 시리즈에 함수 적용하기
# 
# 시리즈 객체에 `apply()` 메서드를 적용하면 모든 원소를 함수에 적용하여 결과값을 반환한다.
# 
# - `series.apply(함수)`
# 
# 먼저 펭귄 데이터에서 'bill_length_mm' 열만 선택해 샘플 시리즈 객체를 만들어 보자.

# In[95]:


import seaborn as sns

df = sns.load_dataset('penguins')
bill_length_mm = df['bill_length_mm']

bill_length_mm.head()


# 해당 시리즈 원소들의 제곱근을 구해보도록 하겠다.

# In[96]:


import numpy as np

result = bill_length_mm.apply(np.sqrt)
result.head()


# `numpy` 패키지의 `sqrt()` 함수는 제곱근을 구해준다. 먼저 `apply()` 메서드 내부에 해당 함수를 입력하면, 'bill_length_mm' 시리즈의 모든 원소들에 함수가 적용되어 제곱근이 구해진다. 이번에는 함수를 새롭게 만든 후 시리즈에 적용해보도록 하자.

# In[97]:


def mm_to_cm(num):
    return num / 10

result_2 = bill_length_mm.apply(mm_to_cm)
result_2.head()


# `mm_to_cm()` 함수는 숫자를 입력하면 10으로 나눈 결과를 반환한다. 위와 동일하게 `apply()` 메서드 내부에 해당 함수를 입력하면 시리즈의 모든 원소가 10으로 나누어진다.
# 
# ### 데이터프레임에 함수 적용하기
# 
# 데이터프레임에 `apply()` 메서드를 적용하면 모든 열 혹은 행을 하나씩 분리하여 함수에 각 원소가 전달된 후 값이 반환된다. 각 열 혹은 행에 함수를 적용하는 법은 다음과 같다.
# 
# - 각 열에 적용: `DataFrame.apply(함수)` 혹은 `DataFrame.apply(함수, axis = 0)`
# - 각 행에 적용: `DataFrame.apply(함수, axis = 1)`
# 
# 먼저 펭귄 데이터셋에서 숫자로만 이루어진 열을 선택해보자.

# In[98]:


df_num = df[['bill_length_mm', 'bill_depth_mm',
             'flipper_length_mm', 'body_mass_g']]
df_num.head()


# 이제 위 데이터프레임에 `apply()` 메서드를 이용해 최대값을 구하는 `max()` 함수를 적용해본다. 먼저 각 열에 함수를 적용해보자.

# In[99]:


df_num.apply(max)
# df_num.apply(max, axis=0)


# `apply(max)` 혹은 `apply(max, axis=0)`를 입력하면 각 열 별로 최대값을 구한다. 이번에는 각 행에 함수를 적용해보자.

# In[100]:


df_num.apply(max, axis=1)


# 함수를 적용하는 방향을 의미하는 `axis`에 1을 입력하면 각 행에 함수를 적용한다. 즉 첫번째 행에서 최대값은 3750.0, 두 번째 행에서 최대값은 3800.0이 계산된다.
# 
# 시리즈와 마찬가지로 함수를 직접 만든 후 이를 적용할 수도 있다. 각 열에서 결측치가 얼마나 있는지 확인해보자.

# In[101]:


def num_null(data):
    null_vec = pd.isnull(data)
    null_count = np.sum(null_vec)

    return null_count

df_num.apply(num_null)


# 1. `isnull()` 함수는 결측치 여부를 판단하며, 결측치면 True, 아니면 False를 반환한다.
# 2. True는 1, False는 0과 매칭되므로, `sum()` 함수를 통해 위에서 계산된 값을 더하면 True에 해당하는 값이 더해져 결측치의 갯수를 의미한다.
# 3. `apply()` 메서드를 통해 각 열에 해당 함수를 적용한다.
# 
# 모든 열에서 결측치가 2개씩 있는 것이 확인된다.
# 
# ## 그룹 연산하기
# 
# 데이터를 특정 기준에 따라 그룹으로 나눈 후 처리하는 작업을 그룹 연산이라고 한다. 그룹 연산은 일반적으로 3단계 과정으로 이루어진다.
# 
# - 분할(split): 데이터를 특정 기준에 따라 분할
# - 적용(apply): 데이터를 집계, 변환, 필터링하는 메서드 적용
# - 결합(combine): 적용의 결과를 하나로 결합
# 
# ```{figure} image/eda/group.png
# ---
# name: group
# ---
# 그룹 연산의 개념
# ```
# 
# {numref}`group`은 그룹 연산의 개념을 그림으로 나타낸 것이다. 먼저 데이터프레임에서 'Col 1'이 A, B, C인 데이터 별로 그룹을 나눈 후, 각 그룹에서 'Col 2'의 합을 구한다. 마지막으로 계산된 결과를 하나로 합친다. 펭귄 데이터셋을 통해 그룹 연산을 배워보도록 하자.

# In[102]:


import seaborn as sns

df = sns.load_dataset('penguins')
df.head()


# ### 그룹 나누기
# 
# 먼저 'species'에 따라 데이터의 그룹을 나눠주도록 하며, `groupby()` 메서드를 사용한다.

# In[103]:


df_group = df.groupby(['species'])

df_group


# In[104]:


df_group.head(2)


# `groupby()` 메서드 내에 기준이 되는 열을 입력하면 그룹 객체가 만들어진다. 현재는 분할만 이루어진 상태이므로 데이터를 출력해도 기존의 데이터프레임과는 크게 차이가 나지 않는다.

# In[105]:


for key, group in df_group:
    print(key)
    display(group.head(2))


# 그러나 for문을 이용해 그룹객체의 이름과 데이터를 확인해보면 species인 Adelie, Chinstrap, Gentoo에 따라 데이터가 분할되어 있다.
# 
# ### 그룹 별 연산하기
# 
# 원하는 조건에 따라 그룹을 나누었다면, 그룹 별 연산을 해보자. 먼저 그룹 별 평균을 구해보도록 한다.

# In[106]:


df_group.mean()


# 그룹 객체에 `mean()` 메서드를 적용하면 각 그룹 별 평균이 계산된다. 이 외에도 `groupby()`와 함께 pandas에 내장되어 있는 다양한 집계 메서드를 사용할 수 있다.
# 
# ```{table} 판다스 내 집계 메서드
# :name: method
# | 메서드 | 기능 |
# | --- | --- |
# | `count` | 누락값을 제외한 데이터 수 |
# | `size` | 누락값을 포함한 데이터 수 |
# | `mean` | 평균 |
# | `std` | 표준편차 | 
# | `var` | 분산 |
# | `min` | 최소값 |
# | `max` | 최대값 | 
# | `quantile(q=0.25)` | 백분위수 25% |
# | `quantile(q=0.50)` | 백분위수 50% |
# | `quantile(q=0.75)` | 백분위수 75% |
# | `sum` | 전체 합 |
# | `describe` | 데이터 수, 평균, 표준편차, 최소값, 백분위수(25, 50, 75%), 최대값 반환 |
# | `first` | 첫번째 행 반환 |
# | `last` | 마지막 행 반환 |
# | `nth` | n번째 행 반환 |
# ```
# 
# 그룹의 기준을 하나가 아닌 여러 열로 설정하는 것 역시 가능하다. 이번에는 'species'와 'sex'에 따른 평균을 구해보도록 하자.

# In[107]:


df.groupby(['species', 'sex']).mean()


# 기준으로 삼고 싶은 열들을 `groupby()` 메서드 내에 리스트 형태로 입력한 후 평균을 구했다. 멀티 인덱스(MultiIndex) 형태로 결과가 반환되며, 같은 종 내에서도 수컷(Male)이 암컷(Female)보다 크기나 무게가 큰 것을 쉽게 비교할 수 있다.
# 
# 집계 연산을 처리하는 함수를 사용자가 직접 만든 후 그룹 객체에 적용하고자 할 때는 `agg()` 메서드를 사용한다. 예제로 최대값과 최소값의 차이를 계산하는 함수를 만든 후 각 그룹별로 적용해보도록 하자.

# In[108]:


def min_max(x):
    return x.max() - x.min()

df.groupby(['species'])['bill_length_mm'].agg(min_max)


# 먼저 최대값과 최소값의 차이를 구하는 `min_max()`  함수를 만들었다. 그 후 'species' 별로 그룹을 나눈 후, 'bill_length_mm' 열만 선택한다. `agg()` 메서드 내에 해당 함수를 입력하면 각 그룹 별로 함수가 적용되었다. `agg()` 메서드를 사용하면 한번에 여러개의 집계 연산을 처리할 수도 있다.

# In[109]:


df.groupby(['species']).agg(['max', 'min'])


# `agg()` 메서드 내에 원하는 집계 연산을 리스트 형태로 입력하면 일괄적으로 적용이 된다. 각 열마다 다른 종류의 함수를 적용할 수도 있다.

# In[110]:


df.groupby(['species']).agg({'bill_length_mm': ['max', 'min'],
                            'island': ['count']})


# `agg()` 메서드 내에 `{열 : 함수}` 형태의 딕셔너리로 입력하면 열마다 다른 종류의 함수를 적용할 수도 있다. 'bill_length_mm' 열은 max와 min값을 구했으며, 'island' 열은 count를 구했다.
# 
# `agg()` 메서드를 이용할 경우 그룹 별로 연산을 위한 함수를 적용하고 연산 결과를 집계하여 반환하였다. 반면 `transform()` 메서드를 이용할 경우 그룹 별로 함수를 적용하는 것은 동일하지만, 그 결과를 본래의 행 인덱스와 열 인덱스를 기준으로 반환한다. 따라서 원본 데이터프레임과 같은 형태로 변형하여 정리를 한다.

# In[111]:


df.groupby(['species'])['bill_length_mm'].transform('mean')


# 'species' 별로 그룹을 나눈 후 'bill_length_mm' 열을 선택하였다. 그 후 `transform()` 매서드를 통해 평균을 구하면, 각 species 별 평균이 집계되는 것이 아닌 원래의 행 인덱스와 열 인덱스에 결과가 반환된다. 이러한 점을 응용해 그룹 별 z-score를 계산해보도록 하자. z-score란 각 데이터의 값이 평균으로부터 얼마나 떨어져 있는지를 나타내는 수치로써, 각 원소를 평균으로 나눈 후 이를 표준편차로 나눈다.
# 
# $$z = \frac{x-\mu}{\sigma}$$ 
# 
# 각 그룹 별 'bill_length_mm'의 z-score를 구해보도록 하자.

# In[112]:


def z_score(x):
    z = (x - x.mean()) / x.std()
    return(z)

df.groupby(['species'])['bill_length_mm'].transform(z_score)


# 먼저 수식에 맞춰 z-score를 계산하는 함수를 만든다. 그 후 'species' 열 별로 그룹을 나눈 후 'bill_length_mm' 열만 선택하여 `transform()` 메서드 내에 `z_score()` 함수를 적용한다. 이를 통해 각 그룹 별 평균과 표준편차를 이용해 모든 원소의 z-score가 계산되며, 결과는 원래의 행 인덱스 순서에 반환된다.
# 
# `apply()` 메서드를 그룹 객체에 적용할 수도 있다.

# In[113]:


df.groupby(['species'])['bill_length_mm'].apply(min)


# 그룹을 나눈 후 `apply()` 메서드 내에 `min`을 입력하면 각 그룹 별로 'bill_length_mm' 열의 최소값이 나타난다. 이번엔 앞서 만든 `z_score()` 함수를 적용해보자. 

# In[114]:


df.groupby(['species'])['bill_length_mm'].apply(z_score)


# `transform()` 메서드를 이용한 것과 결과가 동일하다.
# 
# 그룹 객체에 `filter()` 메서드를 적용하면 조건에 해당하는 그룹만을 반환한다. 위의 예에서 'bill_length_mm'의 평균이 40 이상이 그룹만 찾아보도록 하자.

# In[115]:


df.groupby(['species'])['bill_length_mm'].mean()


# 먼저 species 별 'bill_length_mm'의 평균은 위와 같다. Chinstrap와 Gentoo 종의 평균이 40 이상이다.      

# In[116]:


df.groupby(['species']).filter(lambda x: x['bill_length_mm'].mean() >= 40)


# species 별로 그룹은 나눈 후 `filter()` 메서드 내에 조건식을 입력한다. lambda 함수를 통해 조건을 정의하며, 'bill_length_mm' 열의 평균이 40 이상인 조건을 입력한다. 결과를 살펴보면 Adelie 종은 평균이 40 미만이므로 제외되고, Chinstrap와 Gentoo 종의 데이터만 반환된다.
# 
# ## 시계열 데이터 다루기
# 
# 시계열 데이터(time series data)란 시간을 기준으로 측정된 자료를 말하며, 주가나 재무제표 등 투자에 쓰이는 대부분의 데이터가 시계열 데이터라고도 볼 수 있으므로 이를 다루는 법에 알 필요가 있다. 앞서 datetime 패키지에서 제공하는 datetime 객체를 통해 날짜와 시간을 다룰수 있었다. pandas에서는 문자열을 datetime 객체로 손쉽게 변환할 수 있으므로 이에 대해 알아보겠다. 먼저 택시 승하차 정보가 담긴 taxis 데이터셋을 불러오도록 하자.

# In[117]:


import seaborn as sns

df = sns.load_dataset('taxis')
df.head()


# 'pickup'과 'dropoff' 열을 살펴보면 시계열 형태처럼 보인다. 한 번 데이터의 형태를 살펴보도록 하자.

# In[118]:


df.info()


# `info()` 메서드를 통해 확인해보면 해당 열의 타입이 object 즉 문자열이다. pandas에서는 `to_datetime()` 메서드를 통해 문자열을 datetime 객체로 변환할 수 있다.

# In[119]:


df['pickup'] = pd.to_datetime(df['pickup'])
df['dropoff'] = pd.to_datetime(df['dropoff'])

df.info()


# 두 열의 타입이 'datetime64[ns]' 즉 datetime64 객체로 변하였다.
# 
# 이번에는 'pickup' 열에서 연도에 해당하는 정보만 추출해보도록 하자. 먼저 첫번째 행의 '2019-03-23 20:21:09'에서 연도를 추출하는 법은 다음과 같다.

# In[120]:


df['pickup'][0].year


# 원소의 끝에 `year`를 붙여주면 연도에 해당하는 값이 추출된다. 이 외에도 `month`, `day` 등을 통해 월과 일을 추출할 수도 있다. 그렇다면 'pickup' 열에 존재하는 모든 데이터의 연도를 추출하려면 어떻게 해야할까? `dt` 접근자를 사용하면 datetime 타입의 열에 한 번에 접근할 수 있다.

# In[121]:


df['year'] = df['pickup'].dt.year
df['month'] = df['pickup'].dt.month
df['day'] = df['pickup'].dt.day

df[['pickup', 'year', 'month', 'day']].head()


# 먼저 열을 의미하는 `df['pickup']` 뒤에 `dt` 접근자를 붙여준 후, 추출하고자 하는 정보(year, month, day)를 입력한다. 그 결과 년, 월, 일에 해당 하는 정보만이 추출되었다.
# 
# 현재는 데이터가 시간 순서대로 정렬되어 있지 않으므로, 'pickup' 열을 기준으로 정렬을 해주도록 한다.

# In[122]:


df.sort_values('pickup', inplace=True)
df.reset_index(drop=True, inplace=True)

df.head()


# 1. `sort_values()` 메서드를 통해 'pickup' 열을 기준으로 데이터를 오름차순으로 정렬한다.
# 2. `reset_index()` 메서드를 통해 행 인덱스를 초기화한다.
# 
# 이번에는 'pickup'열과 'dropoff' 열의 차이, 즉 운행시간을 계산해보도록 하자.

# In[123]:


df['dropoff'] - df['pickup']


# 두 열 모두 datetime 객체이므로 시간에 대한 연산이 가능하다. 첫 번째 행의 경우 '2019-02-28 23:32:35' 에서 '2019-02-28 23:29:03'를 뺀 값인 '0 days 00:03:32' 즉 3분 32초가 계산된다. 
# 
# 이번에는 'pickup' 열을 행 인덱스로 변경해보자.

# In[124]:


df.set_index('pickup', inplace=True)

df.head()


# `set_index()` 메서드를 통해 'pickup' 열을 행 인덱스로 설정하였다. 인덱스의 타입을 확인해보도록 하자.

# In[125]:


df.index


# 인덱스가 'DatetimeIndex' 형태라는 것을 알 수 있다. datetime 객체를 데이터프레임의 행 인덱스로 설정하면 원하는 날짜 혹은 시간의 데이터를 바로 추출할 수 있어 매우 편리하다. 해당 데이터는 2019년 2월 28일부터 2019년 3월 31일까지의 정보가 있으며, 이 중에서 2019년 2월에 해당하는 정보만 선택해보도록 하자.

# In[126]:


df.loc['2019-02']


# loc 인덱서 내부에 2019년 2월을 의미하는 '2019-02'를 입력하니, 해당 시점의 데이터만 출력되었다. 이번에는 2019년 3월 1일부터 2019년 3월 2일까지의 데이터를 선택해보자.

# In[127]:


df.loc['2019-03-01':'2019-03-02']


# 인덱서에 슬라이스 형태를 입력하면 이에 해당하는 기간의 데이터만 선택된다.
# 
# ### 시계열 데이터 만들기
# 
# 앞서 `range()` 함수를 통해 숫자(정수) 리스트를 만들었듯이, pandas의 `date_range()` 함수를 통해 여러 개의 날짜가 들어있는 배열 형태의 시계열 데이터를 만들 수 있다. 예제로 2021년 1월부터 2021년 12월까지 한 달 간격으로 시계열 데이터를 만들어보자.

# In[128]:


pd.date_range(start='2021-01-01',
              end='2021-12-31',
              freq='M')


# start는 시작일, end는 종료일, freq는 간격을 뜻한다. `date_range` 함수의 `freq`에는 매우 다양한 종류가 있다.
# 
# ```{table} freq 옵션 종류
# :name: freq
# | 옵션 | 설명 |
# | --- | --- | 
# | B | 비즈니스 데이(휴일 제외) |
# | D | 일 |
# | W | 주 |
# | M | 월말 |
# | BM | 월 마지막 비즈니스 데이 |
# | MS | 월초 |
# | Q | 분기말 |
# | BQ | 분기 시작 비즈네스 데이 |
# | QS | 분기초 |
# | BQS | 분기 시작 비즈니스 데이 |
# | A | 연말 |
# | BA | 연 마지막 비즈니스 데이 |
# | AS | 연초 |
# | BAS | 연 시작 비즈네스 데이 |
# | H | 시간 |
# | T | 분 |
# | S | 초 |
# ```
# 
# 이 외에도 훨씬 많은 옵션이 있으며, 복잡한 형태의 시계열 데이터를 만들 수도 있다.

# In[129]:


pd.date_range(start='2021-01-01',
              end='2021-01-31',
              freq='3D')


# 3D는 3일을 뜻한다. 즉 2021년 1울 1일부터 3일 주기의 시계열 데이터가 만들어진다.

# In[130]:


pd.date_range(start='2021-01-01',
              end='2021-01-31',
              freq='W-MON')


# W는 주를 뜻하고 MON은 월요일을 뜻한다. 즉 매주 월요일에 해당하는 날짜가 시계열 데이터로 만들어진다.

# In[131]:


pd.date_range(start='2021-01-01',
              end='2021-12-31',
              freq='WOM-2THU')


# WOM는 week of month를, 2THU는 둘째주 목요일을 뜻한다. 즉 WOM-2FRI는 매월 둘째주 목요일에 해당하는 날짜가 시계열 데이터로 만들어진다.
