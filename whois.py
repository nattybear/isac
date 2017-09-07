#!/usr/bin/python3

from urllib.request import urlopen
from sys import argv
from json import loads

def get(ip):
	# %s를 이용해서 url 폼을 만든다.
	urlform = 'http://whois.kisa.or.kr/openapi/ipascc.jsp?query=%s&key=%s&answer=json'
	# 발급받은 키는 외부에 공개하면 곤란하다.
	# 따라서 설정 파일을 따로 두고 키값을 읽어올까 생각을 해봤는데
	# 파일 포인터를 열고 닫는데에 시간이 걸리기 때문에
	# 좋은 방법은 아닌 것 같다.
	key = '2016071413065956652873'
	# % 연산자를 이용해서 url 폼에 아이피와 키를 넣는다.
	url = urlform % (ip, key)
	u = urlopen(url)
	# url 객체는 데이터를 바이트 객체로 받아오기 때문에
	# decode 함수를 이용해서 utf-8로 적절히 디코딩 해준다.
	b = u.read().decode('utf-8')
	# url 객체를 닫아준다.
	# url 객체도 열고 닫을 때마다 시간이 소요 될텐데
	# 여러개의 아이피를 한번에 쿼리 할 수 있는 API가 아쉽다.
	u.close()
	# json 모듈의 loads 함수를 이용하면
	# json 문자열 객체를 파이썬 딕셔너리 객체로 변환 할 수 있다.
	j = loads(b)
	# 국가 코드를 리턴한다.
	try:
		return j['whois']['countryCode']
	except KeyError as e:
		print(ip, j)
		return 0

if __name__ == '__main__':
	cc = get(argv[1])
	print(cc)
