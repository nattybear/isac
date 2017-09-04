#!/usr/bin/python3
# Cyber Threat Information

from docx import Document
from sys import argv
from isac import ipcountry, insert, con

doc = Document(argv[1])

# "IP Address"라는 문자열이 있는 테이블 번호와
# 칼럼의 번호를 파악하고 리스트에 튜플로 저장한다.
ipindex = []
for i, table in enumerate(doc.tables):
	for j, head in enumerate(table.rows[0].cells):
		if "IP Address" in head.text:
			ipindex.append((i, j))

# 위에서 조사한 테이블 번호와 칼럼 번호를 이용해서
# 문서의 모든 아이피 주소를 담은 리스트를 만든다.
iplist = []
for table, col in ipindex:
	cells = doc.tables[table].columns[col].cells
	for cell in cells:
		if "IP Address" not in cell.text:
			iplist.append((cell.text,))

ip = ipcountry(iplist)
insert(ip, "ip")

con.commit()
con.close()
