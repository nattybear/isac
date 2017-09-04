#!/usr/bin/python3
# Cyber Threat Information

from docx import Document
from sys import argv

doc = Document(argv[1])

index = []

# "IP Address"라는 문자열이 있는 테이블 번호와
# 칼럼의 번호를 파악하고 리스트에 튜플로 저장한다.
for i, table in enumerate(doc.tables):
	for j, head in enumerate(table.rows[0].cells):
		if "IP Address" in head.text:
			index.append((i, j))

print(index)
