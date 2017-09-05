#!/usr/bin/python3
# Cyber Threat Information

from docx import Document
from sys import argv
from isac import ipcountry, insert, con

doc = Document(argv[1])

# "IP Address"라는 문자열이 있는 테이블 번호와
# 칼럼의 번호를 파악하고 리스트에 튜플로 저장한다.
# "Attack Type"도 같은 원리로 동작.
ipindex = []
attacktypeindex= []
for i, table in enumerate(doc.tables):
	for j, head in enumerate(table.rows[0].cells):
		if "IP Address" in head.text:
			ipindex.append((i, j))
		if "Attack Type" in head.text:
			attacktypeindex.append((i, j))

# 테이블과 칼럼 번호가 적혀 있는 인덱스를 튜플로 받고
# 칼럼 이름을 인자로 넣어주면
# 테이블에서 해당 칼럼의 데이터만 모아서 리스트로 리턴
def parsecol(index, name):
	t = []
	for table, col in index:
		cells = doc.tables[table].columns[col].cells
		for cell in cells:
			if name not in cell.text:
				t.append((cell.text))
	return t

#ip = ipcountry(iplist)
#insert(ip, "ip")

#con.commit()
#con.close()

t = parsecol(ipindex, "IP Address")
print(t)
