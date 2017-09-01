#!/usr/bin/python3

# 범용 스크립트로 사용이 가능하다.
# 칼럼명을 명시해야 하는 경우에도
# 두번째 인자로 테이블명과 함께 테이블명을 입력하면 그만이다.

from sqlite3 import connect, IntegrityError
from sys import argv

# 첫번째 인자는 CSV 파일의 이름
# 두번째 인자는 데이터를 입력할 테이블의 이름
fileName = argv[1]
tableName = argv[2]

f = open(fileName)
# 우선 파일의 첫행만 읽어온다.
# 쉼표를 구분으로 데이터를 나눠서 칼럼의 개수를 알아낸다.
b = f.readline()
columNum = len(b.split(','))

# 파일 포인터를 다시 맨 앞으로 보내고
# 파일의 전체 내용을 다시 읽는다.
# 파일 포인터는 닫아준다.
f.seek(0)
b = f.readlines()
f.close()

# 인자로 받은 테이블 이름과 칼럼의 개수를
# 쿼리에 반영하기 위해 폼을 만든다.
qryForm = 'INSERT INTO %s VALUES (%s)'
# 빈 리스트를 하나 만들고
# 칼럼의 개수만큼 물음표를 넣는다.
values = []
for i in range(columNum): values.append('?')
# 물음표 사이에 쉼표를 넣는다.
values = ','.join(values)
# 쿼리를 완성한다.
qry = qryForm % (tableName, values)

# 데이터베이스에 연결한다.
con = connect('blacklist.db')
cur = con.cursor()

for i in b:
	# 개행을 제거
	t = i.replace('\n', '')
	# 데이터를 쉼표로 구분
	t = t.split(',')
	# 데이터베이스에 데이터를 입력
	try:
		cur.execute(qry, t)
	except IntegrityError as e:
		print(e, t)
		continue

con.commit()
con.close()
