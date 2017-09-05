#!/usr/bin/python3

from sqlite3 import connect, IntegrityError
from bs4 import BeautifulSoup
from sys import argv
from whois import get
import re

# 데이터베이스에 연결한다.
# 함수 안에 선언하면 데이터가 입력 될 때마다
# 연결을 하기 때문에 속도면에서 손해이므로
# 함수 밖에서 먼저 연결 객체를 생성한다.
con = connect('blacklist.db')
cur = con.cursor()

# 외래키 지원 옵션을 활성화하기 위한 쿼리
cur.execute("PRAGMA foreign_keys = ON;")

# 입력으로 테이블 번호를 받는다.
# tbody 태그를 모두 찾은 뒤에
# 입력 받은 번호에 해당하는 테이블 중에서
# tr 태그만 모아서 리스트로 반환한다.
def tr(num):
	a = s.find_all('tbody')
	b = a[int(num)]
	c = b.find_all('tr')
	return c

# 첫번째 인자로 tr 태그의 리스트를 받는다.
# 입력된 리스트 중에 span 태그만 모아서
# 하나의 리스트로 반환한다.
def span(_list):
	# 전체 결과를 담을 임시 리스트를 생성
	t = []
	# 파싱 할 칼럼 번호를 지정
	# 테이블 헤더는 제외
	for i in _list[1:]:
		span = i.find_all('span')
		ip = span[1].string
		attacktypename = span[3].string
		t.append((ip, attacktypename))
	return t

# (ip, 공격유형이름) 데이터를 넣으면
# (날짜, 아이피, 공격유형아이디, 출처아이디) 형태를 리턴
# 이 함수가 준 데이터는 insert 함수에서 사용 가능
def make_row(data):
	t = []
	for i in data:
		ip = i[0]
		attacktypename = i[1]
		# 공격유형에 '악성코드' 문자열이 있으면
		# 레벨에 fatal(1)을 할당하고
		# 그렇지 않으면 그냥 warning(4)을 할당한다.
		level = 4
		if '악성코드' in attacktypename: level = 1
		# 아이피와 공격유형에 해당하는 공격유형 아이디 값을 데이터베이스에 넣기 위한 쿼리를 작성
		cur.execute('SELECT attacktypeid FROM attacktype WHERE attacktypename="%s"' % attacktypename)
		try:
			attacktypeid = cur.fetchone()[0]
		except TypeError as e:
			print(e, i)
			continue
		# 4번째 칼럼에 레벨아이디를 입력한다.
		# 스키마가 변경되었기 때문이다.
		t.append((date, ip, attacktypeid, 1, level))
	return t

# 전자적 침해 시도에서 아이피 주소와 공격 유형을 파싱하는 정규식 함수
# 테이블의 태그를 이용하지 않고 처음부터 끝까지 정규식만을 이용해서 작성
# 테이블 칼럼이 기존 테이블과 다르기 때문에 이렇게 작성함
def getip(text):
	p = re.compile(r"(\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}) [(].{,750}11pt;'>&nbsp;(.+?)</span></p>", re.DOTALL)
	m = p.findall(text)
	return m

# 피싱/파밍사이트 정규식
def phising(text):
	p = re.compile('(\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}) [(].{,10}[)].{20}<td val', re.DOTALL)
	m = p.findall(text)
	t = []
	for i in m:
		t.append((i, '피싱사이트'))
	return t

# ip만을 찾는 정규식 작성
# 모든 ip를 전부 찾아서 ip 테이블에 데이터 입력
def getallip(text):
	p = re.compile('>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?:<| )')
	m = p.findall(text)
	l = []
	for i in m:
		l.append((i,))
	return l

# 아이피 리스트를 받아서 국가코드를 붙여서 리턴 
# 잘 쓰지 않아던 list comprehension을 써봤다.
# 확실히 코드가 짧아지긴 한다.
def ipcountry(data): return [(i[0], get(i[0])) for i in data]

# 데이터베이스에 데이터를 입력하기 위한 함수 작성
# 이 함수에 넣을 데이터는 하나의 레코드에 칼럼이 하나라도
# 튜플 형식으로 넣어야 한다.
def insert(data, table):
	length = len(data[0])
	question = []
	for i in range(length): question.append('?')
	question = ','.join(question)
	tmp = "INSERT INTO %s VALUES (%s)" % (table, question)
	for i in data:
		try:
			cur.execute(tmp, i)
		except IntegrityError as e:
			print(e, i)
			continue

def main():
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

	# 모든 아이피를 추출해서 데이터베이스에 데이터를 입력
	ip = ipcountry(getallip(b))
	insert(ip, "ip")

	# 요주의 IP 탐지현황은 4번째 테이블이다.
	# 해당 테이블을 데이터베이스에 입력한다.
	l1 = make_row(span(tr(4)))
	# 신규 요주의 IP는 6번째 테이블이다.
	l2 = make_row(span(tr(6)))
	# 전자적 침해시도 주요 내역 파싱
	l3 = make_row(getip(b))
	l4 = make_row(phising(b))
	l = l1 + l2 + l3 + l4
	insert(l, '"ip/attacktype/src"')
	
	# 마찬가지 이유로 데이터베이스의 잦은 입출력 방지를 위해서
	# 모든 작업이 끝나고 마지막에 데이터베이스 연결을 끊는다.
	con.commit()
	con.close()
	
if __name__ == '__main__':
	main()
