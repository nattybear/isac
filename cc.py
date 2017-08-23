#!/usr/bin/python3

from sys import argv
from sqlite3 import connect, IntegrityError

f = open(argv[1])
# readlines 함수를 이용하면 자연스럽게
# 행별로 리스트를 만들 수 있다.
b = f.readlines()

# 데이터베이스 이름을 하드코딩했다.
con = connect('blacklist.db')
cur = con.cursor()

qry = 'INSERT INTO country VALUES (?,?)'

for i in b:
	# 데이터 중에서 국가 이름에 쉼표(,)가 들어가는
	# 데이터가 있기 때문에 split 함수를 사용하지 못함
	# 따라서 첫번째 쉼표의 위치를 찾아서
	# 해당 위치를 기준으로 앞뒤로 데이터를 구분함
	idx = i.find(',')
	cc = i[:idx]
	name = i[idx+1:]
	t = cc, name
	try:
		cur.execute(qry, t)
	# 중복 방지를 위해서 에러 처리를 이용함
	# 주키를 국가코드로 스키마를 작성했기 때문에
	# 같은 국가코드가 입력되면 에러가 발생한다.
	# 에러가 발생하더라도 다음 데이터에 대한 작업을
	# 계속 할 수 있도록 continue를 사용함
	# 에러 메세지에는 어떤 데이터가 중복되는지도 표시하므로
	# 트러블슈팅이 가능하고 새로운 데이터를 추가하고 싶을 때는
	# CSV 파일에 추가만 하더라도 데이터베이스 입력시 알아서
	# 중복 제거가 가능함
	except IntegrityError as e:
		print(e, t)
		continue

# 모든 데이터 입출력이 종료되면
# commit을 한다.
# 파일이든 데이터베이스이든 열고 닫는 행위는
# 최소화해야 프로그램의 속도가 느려지지 않을 것이다.
con.commit()
con.close()
