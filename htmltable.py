#!/usr/bin/python3

from sys import argv
from bs4 import BeautifulSoup
from sqlite3 import connect

# ISAC 파일 인코딩은 UTF-16 리틀 엔디안이다.
f = open(argv[1], encoding='utf-16-le')
b = f.read()
f.close()

# 뷰티풀 스프 객체를 만든다.
s = BeautifulSoup(b, 'html.parser')

# 첫번째 테이블은 버린다.
tables = s.find_all('table')[1:]

lists = []
for table in tables:
	trlen = len(table.find_all('tr'))
	rows = []
	# 행의 개수가 2개 이상인 테이블만 작업한다.
	if trlen > 1:
		for tr in table.find_all('tr'):
			col = []
			for td in tr.find_all('td'):
				col.append(td.span.string)
			# 칼럼을 모두 모아서 한 열로 저장한다.
			rows.append(col)
	# 행을 모두 모아서 하나의 테이블로 저장한다.
	lists.append(rows)

# 사전을 정의한다.
# 행 첫째 줄의 항목을 검사해서
# 어느 테이블에 입력할지 결정한다.
# 아래 없는 항목은 따로 조건문을 이용한다.
dic = {
	'탐지건수'	: '요주의 IP 탐지현황',
	'공격 IP'	: '전자적 침해시도 주요 내역',
	'대상'		: '피싱/파밍사이트 내역' }

for table in lists:
	
