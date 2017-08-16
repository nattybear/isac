#!/usr/bin/python3

from sys import argv

# 프로그램의 인자로 htm 파일을 받는다.
# htm 파일을 읽을 때는 'utf-16-le' 인코딩으로 읽는다.
f = open(argv[1], encoding='utf-16-le')
b = f.read()
f.close()
