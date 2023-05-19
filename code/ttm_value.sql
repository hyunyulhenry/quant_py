# 삼성전자 분기별 매출액
use stock_db;

select * from kor_fs
where 계정 = '매출액' and 종목코드 = '005930' and 공시구분 = 'q';

# 4개 있으면 평균 or 합 구하기
select 계정, 기준일, 종목코드,	
    # PSR, PCR, PER, DY 계산
    case when 4 = count(*)
		over(partition by 계정 order by 기준일 rows between 3 preceding and current row)
        and 계정 in ('매출액', '영업활동으로인한현금흐름', '지배주주순이익', '배당금지급(-)')
    then 
		sum(값)
		over(partition by 계정 order by 기준일 rows between 3 preceding and current row)	
    # PBR 계산
    when 4 = count(*)
		over(partition by 계정 order by 기준일 rows between 3 preceding and current row)
        and 계정 in ('자본')
    then 
		avg(값)
		over(partition by 계정 order by 기준일 rows between 3 preceding and current row)		
	end
    as ttm
from kor_fs 
where 공시구분 = 'q'
and 종목코드 = '005930'
and 계정 in ('매출액', '영업활동으로인한현금흐름', '자본', '지배주주순이익', '배당금지급(-)');

# 최근일만 선택하기
select 종목코드, max(기준일) as 최근일
from kor_fs
where 공시구분 ='q'
group by 종목코드
having 종목코드 = '005930';

# 분기 기준 재무제표의 최근일이 max와 매치하는 값

## 두개 조인
select *,
    # PSR, PCR, PER, DY 계산
    case when 4 = count(*)
		over(partition by a.계정 order by 기준일 rows between 3 preceding and current row)
        and a.계정 in ('매출액', '영업활동으로인한현금흐름', '지배주주순이익', '배당금지급(-)')
    then 
		sum(값)
		over(partition by a.계정 order by 기준일 rows between 3 preceding and current row)	
    
    # PBR 계산
    when 4 = count(*)
		over(partition by 계정 order by 기준일 rows between 3 preceding and current row)
        and a.계정 in ('자본')
    then 
		avg(값)
		over(partition by a.계정 order by 기준일 rows between 3 preceding and current row)		
	end as ttm,
    rank() over (partition by a.계정 order by 기준일) as rnk,
    count(*) over (partition by a.계정) as cnt
from kor_fs as a
where a.공시구분 = 'q'
and a.종목코드 = '005930'
and a.계정 in ('매출액', '영업활동으로인한현금흐름', '자본', '지배주주순이익', '배당금지급(-)');

# 주가랑 붙이기
## DY는 뒤집기

# PSR, PCR, PER
