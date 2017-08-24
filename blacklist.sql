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
	id integer primary key autoincrement,
	name text UNIQUE,
	priority integer
);

CREATE TABLE IF NOT EXISTS detail (
	name text primary key,
	typeid integer,
	FOREIGN KEY(typeid) REFERENCES type(id)
);

CREATE VIEW IF NOT EXISTS type_detail AS SELECT DISTINCT type FROM isac;
