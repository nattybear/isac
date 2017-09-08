#!/usr/bin/python3

from sys import argv
from bs4 import BeautifulSoup

f = open(argv[1], encoding='utf-16-le')
b = f.read()
f.close()

s = BeautifulSoup(b, 'html.parser')
tables = s.find_all('table')

print(tables[0])
