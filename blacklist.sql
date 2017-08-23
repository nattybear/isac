CREATE TABLE IF NOT EXISTS isac (
	date text,
	ip text,
	type text,
	primary key (date, ip, type)
);

CREATE TABLE IF NOT EXISTS country (
	code text primary key,
	name text
);

CREATE TABLE IF NOT EXISTS type (
	id integer primary key,
	name text
);
