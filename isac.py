#!/usr/bin/python3

from sqlite3 import connect, IntegrityError
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

# 데이터베이스에 연결한다.
# 함수 안에 선언하면 데이터가 입력 될 때마다
# 연결을 하기 때문에 속도면에서 손해이므로
# 함수 밖에서 먼저 연결 객체를 생성한다.
con = connect('blacklist.db')
cur = con.cursor()

# 입력으로 테이블 번호를 받는다.
# tbody 태그를 모두 찾은 뒤에
# 입력 받은 번호에 해당하는 테이블 중에서
# tr 태그만 모아서 리스트로 반환한다.
def tr(num):
	a = s.find_all('tbody')
	b = a[int(num)]
	c = b.find_all('tr')
	# 테이블 헤더는 제외하고 리턴
	return c[1:]

# 첫번째 인자로 tr 태그의 리스트를 받는다.
# 두번째 인자로 출력할 칼럼 번호를 받는다.
# 이 함수는 두개의 칼럼만 출력 할 수 있다.
# 입력된 리스트 중에 span 태그만 모아서
# 하나의 리스트로 반환한다.
def span(_list, _tuple):
	# 전체 결과를 담을 임시 리스트를 생성
	t = []
	# 파싱 할 칼럼 번호를 지정
	a, b = _tuple
	for i in _list:
		span = i.find_all('span')
		t.append((span[a].string, span[b].string))
	return t

# 데이터를 데이터베이스에 입력한다.
# 첫번째 인자로 데이터베이스 쿼리를 입력한다.
# 두번째 인자로 입력할 데이터를 받는다.
# 중복 방지를 위해서 에러를 이용한다.
def insert(qry, data):
	for i in data:
		try:
			cur.execute(qry, (date, i[0], i[1]))
		except IntegrityError as e:
			print('[*]', e, i)
			continue

def main():
	l = tr(4)
	d = span(l, (1, 3))
	insert('insert into isac values (?,?,?)', d)
	# 마찬가지 이유로 데이터베이스의 잦은 입출력 방지를 위해서
	# 모든 작업이 끝나고 마지막에 데이터베이스 연결을 끊는다.
	con.commit()
	con.close()
	
if __name__ == '__main__':
	main()
