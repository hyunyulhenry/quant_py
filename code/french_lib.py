import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

url = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Portfolios_Formed_on_OP_CSV.zip'
df_op = pd.read_csv(url, skiprows = 24, encoding='cp1252', index_col = 0)
end_point = np.where(pd.isna(df_op.iloc[:, 2]))[0][0]
df_op_vw = df_op.iloc[0:end_point][['Lo 20', 'Qnt 2', 'Qnt 3', 'Qnt 4', 'Hi 20']].apply(pd.to_numeric)
df_op_cum = np.log(1+df_op_vw/100).cumsum()

plt.rc('font', family='Malgun Gothic')
df_op_cum.plot(figsize = (10, 6), colormap=cm.jet, legend='reverse', title = '수익성별 포트폴리오의 누적 수익률')
plt.show()


## quality value
url = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/25_Portfolios_BEME_OP_5x5_CSV.zip'
df_qv = pd.read_csv(url, skiprows = 21, encoding='cp1252', index_col = 0)
end_point = np.where(pd.isna(df_qv.iloc[:, 2]))[0][0]
df_qv = df_qv.iloc[0:end_point].apply(pd.to_numeric)

# quality
df_qv_quality = df_qv.loc[:, ['LoBM HiOP', 'BM2 OP5', 'BM3 OP5']].mean(axis = 1)
df_qv_value = df_qv.loc[:, ['HiBM LoOP', 'BM5 OP2', 'BM5 OP3']].mean(axis = 1)
df_qv_junk = df_qv.loc[:, ['LoBM LoOP', 'BM1 OP2', 'BM2 OP1', 'BM2 OP2']].mean(axis = 1)
df_qv_best = df_qv.loc[:, ['BM5 OP4', 'HiBM HiOP', 'BM4 OP4', 'BM4 OP5']].mean(axis = 1)

df_qv_bind = pd.concat([df_qv_quality, df_qv_value, df_qv_junk, df_qv_best], axis = 1)
df_qv_bind.columns = ['Quality', 'Value', 'Junk', 'Best']
df_qv_bind_cum = np.log(1+df_qv_bind/100).cumsum()

plt.rc('font', family='Malgun Gothic')
df_qv_bind_cum.plot(figsize = (10, 6), colormap=cm.jet, legend='reverse', title = '퀄리티-밸류별 누적 수익률')
plt.show()

