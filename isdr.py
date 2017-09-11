#!/usr/bin/python3
from sys import argv
from bs4 import BeautifulSoup
from sqlite3 import connect, IntegrityError
from whois import get

# 파일을 열어서 내용을 읽는다.
f = open(argv[1])
b = f.read()
f.close()
b = b.replace('\n', '')
b = b.replace('\t', '')
b = b.replace('&nbsp;', '')

# 뷰티풀 스프 객체를 만든다.
soup = BeautifulSoup(b, 'html.parser')

# 원하는 테이블 번호를 찾는다.
tables = soup.find_all('table')
tableno = 0
for i, table in enumerate(tables):
	for th in table.find_all('th'):
		if 'HASH' in th.string:
			tableno = i

# 데이터만 뽑아서 리스트로 만든다.
rows = []
for tr in tables[tableno].find_all('tr')[1:]:
	tds = []
	for td in tr.find_all('td'):
		cnt = len(list(td.strings))
		t = []
		for s in td.strings:
			t.append(s)
		tds.append(t)
	rows.append(tds)	

con = connect('blacklist.db')
cur = con.cursor()
# 우선 원본 데이터를 그대로 저장할 테이블을 하나 만든다.
# 커밋은 하지 않을 것이다.
# 여기서만 사용하고 저장하지는 않을 것.
sql = '''
	create table if not exists isdr (
		md5 text primary key,
		ip text,
		url text,
		type text
	);'''
cur.execute(sql)
sql = 'insert into isdr values (?,?,?,?)'

# 원본 데이터를 임시 테이블에 그대로 저장함.
# 이제 SQL을 이용해서 데이터를 가공 할 수 있다.
for row in rows:
	t = []
	for td in row:
		t.append('|'.join(td))
	cur.execute(sql, t)

# 해쉬값만 모아서 입력한다.
cur.execute('select md5 from isdr')
sql = 'insert into file values (?)'
for i in cur.fetchall():
	try:
		cur.execute(sql, i)
	except IntegrityError as e:
		print(e, i)
		continue

# 아이피만 모아서 입력한다.
# 아이피는 한 칼럼에 두개 이상인 경우를 처리해야 한다.
cur.execute('select ip from isdr where ip != "N/A"')
sql = 'insert into ip values (?,?)'
for i in cur.fetchall():
		for j in i[0].split('|'):
			c = get(j)
			try:
				cur.execute(sql, (j, c))
			except IntegrityError as e:
				print(e, j, c)

# 해쉬값과 아이피의 관계를 입력한다.
cur.execute('select ip, md5 from isdr where ip != "N/A"')
sql = 'insert into "file/ip" values (?,?)'
for i in cur.fetchall():
	for j in i[0].split('|'):
		try:
			cur.execute(sql, (i[1], j))
		except IntegrityError as e:
			print(e, i[1], j)

# 악성코드 종류를 원본에서 조회하고
# 데이터베이스에 입력한다.
cur.execute('select distinct type from isdr')
sql = 'insert into filetype(filetypename) values (?)'
for i in cur.fetchall():
	try:
		cur.execute(sql, i)
	except IntegrityError as e:
		print(e, i)
		continue

# 해쉬값과 악성코드 종류의 관계를 입력한다.
cur.execute('select md5, type from isdr')
sql1 = 'select filetypeid from filetype where filetypename="%s"'
sql2 = 'insert into "file/type" values (?,?)'
for i in cur.fetchall():
	cur.execute(sql1 % i[1])
	id = cur.fetchone()[0]
	try:
		cur.execute(sql2, (i[0], id))
	except IntegrityError as e:
		print(e, i)
		continue

# 관계형 데이터베이스 작업이 끝나면
# 원본 테이블은 삭제한다.
sql = 'drop table isdr'
cur.execute(sql)

# 모든 작업이 끝나면 데이터베이스 내용을 저장한다.
con.commit()
con.close()
