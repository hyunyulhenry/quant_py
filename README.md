# 파이썬을 이용한 퀀트 투자 포트폴리오 만들기

<img src="https://github.com/hyunyulhenry/quant_py/raw/main/image/cover.png?raw=true"  width="500">

이 곳은 **파이썬을 이용한 퀀트 투자 포트폴리오 만들기**의 코드 저장소 및 질문을 위한 공간입니다.

- [예스24](https://bit.ly/quant_yes)
- [교보](https://bit.ly/quant_kyobo)
- [알라딘](https://bit.ly/quant_aladin)

파이썬이 아닌 R을 사용하시는 분은, "R을 이용한 퀀트 투자 포트폴리오 만들기"를 참조해 주시기 바랍니다.

- [구매처](http://www.yes24.com/Product/Goods/97163849)
- [깃허브](https://github.com/hyunyulhenry/quant_cookbook)

# 강의 영상
👇 책의 강의영상은 **'헨리의 퀀트대학'** 유튜브에서 무료로 보실 수 있습니다. 

[![](https://github.com/hyunyulhenry/quant_py/blob/main/image/search.png?raw=true)](https://www.youtube.com/channel/UCHfiWvw33aSBktAlWICfPKQ?sub_confirmation=1)

# 공지사항 (중요)

2022년 말 야후 파이낸스의 정책이 가격 제공방식이 바뀌었음에도 불구하고, 책에서 사용하는 `pandas_datareader` 패키지가 해당 문제를 완벽하게 수정하지 않고 있습니다.

야후 데이터를 다운로드 받는 다른 패키지인 `yfinance`는 이 문제를 해결하였기 때문에  `pandas_datareader` 패키지가 업데이트 되기까지 `yfinance` 패키지를 override 해주실 것을 권장드립니다. 아래와 같이 세팅해주시면 야후 파이낸스 데이터를 받으실 수 있습니다.

```
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

df = pdr.get_data_yahoo("티커")
```

- yfinance 사용법: https://pypi.org/project/yfinance/
- pandas_datareader 패키지 깃허브: https://github.com/pydata/pandas-datareader

# 질문 및 답변
질문사항은 [Issues](https://github.com/hyunyulhenry/quant_py/issues)에 남겨주시기 바랍니다.

# 책의 구성

#### 여는 글
[지은이 소개 및 머리말](https://github.com/hyunyulhenry/quant_py/blob/main/index.ipynb)

#### Part 1 퀀트와 프로그래밍 기초 배워 보기
1. [퀀트에 대해 알아보기](https://github.com/hyunyulhenry/quant_py/blob/main/quant_intro.ipynb)
2.  [파이썬 기초 배워 보기](https://github.com/hyunyulhenry/quant_py/blob/main/python.ipynb)
3.  [데이터 분석 배워 보기](https://github.com/hyunyulhenry/quant_py/blob/main/eda.ipynb)
4.  [데이터 시각화 배워 보기](https://github.com/hyunyulhenry/quant_py/blob/main/plot.ipynb)
5. [SQL 기초 배워 보기](https://github.com/hyunyulhenry/quant_py/blob/main/sql.ipynb)
6. [파이썬에서 SQL 연결하기](https://github.com/hyunyulhenry/quant_py/blob/main/sql_in_python.ipynb)

#### Part 2 크롤링을 이용한 데이터 수집
7. [크롤링을 위한 웹 기본 지식](https://github.com/hyunyulhenry/quant_py/blob/main/web.ipynb)
8. [정적 크롤링 실습하기](https://github.com/hyunyulhenry/quant_py/blob/main/crawl_basic.ipynb)
9. [동적 크롤링과 정규 표현식](https://github.com/hyunyulhenry/quant_py/blob/main/selenium.ipynb)
10. [국내 주식 데이터 수집](https://github.com/hyunyulhenry/quant_py/blob/main/data_korea.ipynb)
11. [전 세계 주식 데이터 수집하기](https://github.com/hyunyulhenry/quant_py/blob/main/data_global.ipynb)
12. [투자 참고용 데이터 수집](https://github.com/hyunyulhenry/quant_py/blob/main/data_ref.ipynb)

#### Part 3 포트폴리오 구성, 백테스트 및 매매하기
13. [퀀트 전략을 이용한 종목선정](https://github.com/hyunyulhenry/quant_py/blob/main/factor.ipynb)
14. [포트폴리오 구성 전략](https://github.com/hyunyulhenry/quant_py/blob/main/portfolio.ipynb)
15. [트레이딩을 위한 기술적 지표](https://github.com/hyunyulhenry/quant_py/blob/main/technical.ipynb)
16. [백테스팅 시뮬레이션](https://github.com/hyunyulhenry/quant_py/blob/main/backtest.ipynb)
17. [증권사 API 연결과 매매하기](https://github.com/hyunyulhenry/quant_py/blob/main/api_trading.ipynb)

# 연락처
- https://blog.naver.com/leebisu
- leebisu@gmail.com
