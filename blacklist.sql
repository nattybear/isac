BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS ip (
	ip TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS category (
	categoryid INTEGER PRIMARY KEY AUTOINCREMENT,
	categoryname TEXT UNIQUE,
	priority INTEGER
);

INSERT INTO category(categoryname, priority) VALUES ("정보수집", 100);
INSERT INTO category(categoryname, priority) VALUES ("서비스거부", 100);
INSERT INTO category(categoryname, priority) VALUES ("악성코드", 50);
INSERT INTO category(categoryname, priority) VALUES ("피싱", 100);
INSERT INTO category(categoryname, priority) VALUES ("웹공격", 100);

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

COMMIT;
