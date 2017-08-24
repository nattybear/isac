CREATE TABLE IF NOT EXISTS isac (
	date text,
	ip text,
	typeName text,
	primary key (date, ip, typeName)
);

CREATE TABLE IF NOT EXISTS country (
	code text primary key,
	countryName text
);

CREATE TABLE IF NOT EXISTS category (
	categoryId integer primary key autoincrement,
	categoryName text UNIQUE,
	priority integer
);

CREATE TABLE IF NOT EXISTS type (
	typeName text primary key,
	categoryId integer,
	FOREIGN KEY(categoryId) REFERENCES category(categoryId)
);
