CREATE TABLE IF NOT EXISTS ip (
	ip TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS category (
	categoryid INTEGER PRIMARY KEY AUTOINCREMENT,
	categoryname TEXT UNIQUE,
	priority INTEGER
);

CREATE TABLE IF NOT EXISTS subcategory (
	subcategoryid INTEGER PRIMARY KEY AUTOINCREMENT,
	subcategoryname TEXT UNIQUE,
	categoryid INTEGER,
	FOREIGN KEY(categoryid) REFERENCES category(categoryid)
);

CREATE TABLE IF NOT EXISTS ip_subcategory (
	ip TEXT,
	subcategoryid INTEGER,
	FOREIGN KEY(ip) REFERENCES ip(ip),
	FOREIGN KEY(subcategoryid) REFERENCES subcategory(subcategoryid)
);
