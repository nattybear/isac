#!/usr/bin/python3

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
