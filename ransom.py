#!/usr/bin/python3

from sys import argv

def main():
	f = open(argv[1], 'rb')
	lines = f.readlines()
	for i in lines:
		# 아스키는 127까지인데 해당 숫자가 넘어가는 데이터가 존재
		# charmap 인코딩을 사용하면 시스템에서 사용하는 인코딩으로 해석
		i = i.decode('charmap')
		print(i)

if __name__ == '__main__':
	main()
