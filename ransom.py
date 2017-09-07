#!/usr/bin/python3

from sys import argv
from sqlite3 import connect, IntegrityError, ProgrammingError
from datetime import date, timedelta
from re import compile
from whois import get
from isac import con, cur, insert, ipcountry
from urllib.request import urlopen

# 큰 따옴표를 제거하는 함수
def delquo(text): return text.replace('"', '')

# '","'를 구분으로 문자열을 쪼개는 함수
def splitcom(text): return text.split('","')

# 입력된 값이 아이피인지 아닌지 알려주는 함수
def isip(text):
	p = compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
	m = p.search(text)
	return True if m else False

# 문서작성용 멘트에 따른 유형을 매칭한 딕셔너리
dic =	{
	'Payment Site'		: '유해사이트',
	'Distribution Site'	: '악성코드',
	'C2'			: 'C&C 서버'
	}

def main():
	# 쿼리 템플릿을 작성
	sql = 'insert into ransom values (%s)' % ','.join(['?']*10)

	# CSV 파일을 연다.
	# 코드가 완성되면 파일 입력에서
	# 웹 요청으로 변경 예정.
	#f = open(argv[1], 'rb')
	# 웹 요청으로 변경
	f = urlopen('https://ransomwaretracker.abuse.ch/feeds/csv/')
	lines = f.readlines()
	for i in lines:
		# 아스키는 127까지인데 해당 숫자가 넘어가는 데이터가 존재
		# charmap 인코딩을 사용하면 시스템에서 사용하는 인코딩으로 해석
		i = i.decode('charmap')
		# 개행은 삭제한다.
		i = i.replace('\n', '')
		# 주석은 무시한다.
		if i[0] != '#':
			t = list(map(delquo, splitcom(i)))
			try:
				cur.execute(sql, t)
				pass
			# 중복 에러, 외래키 에러
			except IntegrityError as e:
				print(e, t)
				continue
			# 인코딩 에러
			except ProgrammingError as e:
				print(e, t)
				continue

	# 이틀 전 날짜를 구한다.
	ago = date.today() - timedelta(days=3)
	# 쿼리를 작성한다.
	sql = ''' 
		SELECT host, malware, threat, url, ip, firstseen
		FROM ransom
		WHERE firstseen > "%s";''' % ago
	# 쿼리를 실행한다.
	cur.execute(sql)
	# 결과를 받아온다.
	rows = cur.fetchall()
	hostlist = []
	attacktypelist = []
	iplist = []
	urllist = []
	for row in rows:
		host = row[0]
		malware = row[1]
		threat = row[2]
		docu = "%s ransomware %s" % (malware, threat)
		url = row[3]
		ip = row[4]
		day = row[5].split()[0]
		# 모든 호스트를 리스트로 만든다.
		hostlist.append((host,))
		# 모든 문서작성용 멘트를 리스트로 만든다.
		# attacktype 테이블에 입력할 것이다.
		sql = 'SELECT typeid FROM type WHERE typename="%s"' % dic[threat]
		cur.execute(sql)
		typeid = cur.fetchone()[0]
		t = (docu, typeid)
		attacktypelist.append(t)
		# 모든 아이피를 리스트로 만든다.
		# 아이피가 여러개인 경우를 잘 생각해야 한다.
		IPs = ip.split('|')
		for ip in IPs:
			if ip != '':
				iplist.append((ip,))
				# url 테이블에 입력할 데이터를 만든다.
				t = (day, url, ip, typeid, 3, 4, host)
				urllist.append(t)

	# 모은 리스트들을 데이터베이스에 입력한다.
	insert(hostlist, 'host')
	insert(attacktypelist, 'attacktype(attacktypename, typeid)')
	# 아이피 리스트를 (아이피, 국가) 리스트로 변환한다.
	iplist = ipcountry(iplist)
	insert(iplist, 'ip')
	# url 테이블에 데이터를 입력한다.
	insert(urllist, 'url')

	# 데이터베이스 연결을 끊는다.
	con.commit()
	con.close()

if __name__ == '__main__':
	main()
