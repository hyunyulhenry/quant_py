#-*- coding: utf-8 -*-

import pandas_datareader.data as web 
from pandas_datareader.famafrench import get_available_datasets

datasets = get_available_datasets()
datasets[1:20]

df_pbr = web.DataReader('Portfolios_Formed_on_BE-ME', 'famafrench', start = '1900-01-01')
df_pbr[0].head()

import pandas_datareader.data as web 
df_op = web.DataReader('Portfolios_Formed_on_OP', 'famafrench', start = '1900-01-01')


#######
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import re
import pandas as pd
from pandas_datareader.compat import StringIO

url = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Portfolios_Formed_on_OP_CSV.zip'
url = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip'

resp = urlopen(url)
zipfile = ZipFile(BytesIO(resp.read()))
zipfile.namelist()

data = zipfile.open(zipfile.namelist()[0]).read().decode('utf-8','ignore')


datasets, table_desc = {}, []
for i, src in enumerate(data):
    match = re.search(r"^\s*,", src, re.M)  # the table starts there
    start = 0 if not match else match.start()

    df = pd.read_csv(StringIO("Date"))
    try:
        idx_name = df.index.name  # hack for pandas 0.16.2
        df = df.to_period(df.index.inferred_freq[:1])
        df.index.name = idx_name
    except Exception:
        pass
    
    datasets[i] = df

    title = src[:start].replace("\r\n", " ").strip()
    shape = "({0} rows x {1} cols)".format(*df.shape)
    table_desc.append("{0} {1}".format(title, shape).strip())

