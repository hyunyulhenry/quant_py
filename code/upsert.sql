use exam;
# select * from price_2;

# 테이블 만들기
use exam;

CREATE TABLE price_2(
  날짜 varchar(10), 
  티커 varchar(6),
  종가 int,
  거래량 int,
  PRIMARY KEY(날짜, 티커)
);

select * from price_2;

# 데이터 넣기
insert into price_2 (날짜, 티커, 종가, 거래량)
values
('2021-01-02', '000001', 1340, 1000),
('2021-01-03', '000001', 1315, 2000),
('2021-01-02', '000002', 500, 200);

select * from price_2;

# 추가로 넣기
insert into price_2 (날짜, 티커, 종가, 거래량)
values
('2021-01-02', '000001', 1310, 1000),
('2021-01-03', '000001', 1315, 2000),
('2021-01-02', '000002', 500, 200),
('2021-01-03', '000002', 1380, 3000) 
on duplicate key updateus_ticker
종가 = 종가, 거래량 = 거래량;

select * from price_2;

# 수정의 경우
insert into price_2 (날짜, 티커, 종가, 거래량)
values
('2021-01-02', '000001', 1300, 1100),
('2021-01-04', '000001', 1300, 2000)
as new
on duplicate key update
종가 = new.종가, 거래량 = new.거래량;

select * from price_2;

# drop table price_2;
