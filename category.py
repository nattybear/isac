#!/usr/bin/python3

from sys import argv
from sqlite3 import connect, IntegrityError

f = open(argv[1])
b = f.readlines()
f.close()

con = connect('blacklist.db')
cur = con.cursor()

qry = 'INSERT INTO category(categoryName, priority) VALUES (?,?)'

for i in b:
	t = i.replace('\n', '')
	t = t.split(',')
	try:
		cur.execute(qry, t)
	except IntegrityError as e:
		print(e, t)
		continue

con.commit()
con.close()
