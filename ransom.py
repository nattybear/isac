#!/usr/bin/python3

from sys import argv
from sqlite3 import connect, IntegrityError, ProgrammingError

# 큰 따옴표를 제거하는 함수
def delquo(text): return text.replace('"', '')

# '","'를 구분으로 문자열을 쪼개는 함수
def splitcom(text): return text.split('","')

def main():
	# 데이터베이스에 연결한다.
	con = connect('blacklist.db')
	cur = con.cursor()
	# 쿼리를 작성한다.
	sql = 'insert into ransom values (%s)' % ','.join(['?']*10)

	# CSV 파일을 연다.
	# 코드가 완성되면 파일 입력에서
	# 웹 요청으로 변경 예정.
	f = open(argv[1], 'rb')
	lines = f.readlines()
	for i in lines:
		# 아스키는 127까지인데 해당 숫자가 넘어가는 데이터가 존재
		# charmap 인코딩을 사용하면 시스템에서 사용하는 인코딩으로 해석
		i = i.decode('charmap')
		# 개행은 삭제한다.
		i = i.replace('\n', '')
		# 주석은 무시한다.
		if i[0] != '#':
			t = list(map(delquo, i.split(',')))
			try:
				cur.execute(sql, t)
			except IntegrityError as e:
				print(e, t)
				continue
			except ProgrammingError as e:
				print(e, t)
				continue
	
	# 데이터베이스 연결을 끊는다.
	con.commit()
	con.close()

if __name__ == '__main__':
	main()
