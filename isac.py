#!/usr/bin/python3

from bs4 import BeautifulSoup
from sys import argv
import re

# 프로그램의 인자로 htm 파일을 받는다.
# htm 파일을 읽을 때는 'utf-16-le' 인코딩으로 읽는다.
f = open(argv[1], encoding='utf-16-le')
b = f.read()
f.close()

# 등록일을 파싱하기 위한 정규식을 작성
p = re.compile('<td>(\d{4}[.]\d{2}[.]\d{2})</td>')
m = p.search(b)
# date 전역 변수에 등록일을 저장
date = m.group(1)

# html 파싱을 위해 BeautifulSoup 객체를 생성
s = BeautifulSoup(b, 'html.parser')

# 입력으로 테이블 번호를 받는다.
# tbody 태그를 모두 찾은 뒤에
# 입력 받은 번호에 해당하는 테이블 중에서
# tr 태그만 모아서 리스트로 반환한다.
def parse(num):
	a = s.find_all('tbody')
	b = a[int(num)]
	c = b.find_all('tr')
	return c
