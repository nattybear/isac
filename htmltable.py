#!/usr/bin/python3

from sys import argv
from bs4 import BeautifulSoup

# ISAC 파일 인코딩은 UTF-16 리틀 엔디안이다.
f = open(argv[1], encoding='utf-16-le')
b = f.read()
f.close()

# 뷰티풀 스프 객체를 만든다.
s = BeautifulSoup(b, 'html.parser')

# 첫번째 테이블은 버린다.
tables = s.find_all('table')[1:]

for table in tables:
	trlen = len(table.find_all('tr'))
	if trlen > 1:
		print(table.tr.td.span.string)
