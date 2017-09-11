create table ip (
	ip text primary key,
	countrycode text,
	foreign key(countrycode) references country(countrycode)
);

create table attacktype (
	attacktypeid integer primary key autoincrement,
	attacktypename text unique,
	typeid integer,
	foreign key(typeid) references type(typeid)
);

create table type (
	typeid integer primary key autoincrement,
	typename text unique
);
create table level (
	levelid integer primary key autoincrement,
	levelname text unique,
	priority integer
);

create table src (
	srcid integer primary key autoincrement,
	srcname text unique
);

create table "ip/attacktype/src" (
	day text,
	ip text,
	attacktypeid integer,
	srcid integer,
	levelid integer,
	unique(day, ip, attacktypeid, srcid, levelid),
	foreign key(ip) references ip(ip),
	foreign key(attacktypeid) references attacktype(attacktypeid),
	foreign key(srcid) references src(srcid)
	foreign key(levelid) references level(levelid)
);

create table country (
	countrycode text primary key,
	countryname text unique
);

create table file (
	md5 text primary key
);

create table host (
	hostname text primary key,
	hosttype text
);

create table target (
	targetid integer primary key autoincrement,
	targetname text unique
);

create table url (
	url text,
	host text,
	unique(url, host)
	foreign key(host) references host(host)
);

create table ransom (
	firstseen text,
	threat text,
	malware text,
	host text,
	url text,
	status text,
	registrar text,
	ip text,
	asn text,
	country text,
	unique(firstseen, threat, malware, host, url, status, registrar, ip, asn, country)
);

create table "host/type" (
	day text,
	host text,
	attacktypeid integer,
	srcid integer,
	unique(day, host, attacktypeid, srcid),
	foreign key(host) references host(host),
	foreign key(attacktypeid) references attacktype(attacktypeid),
	foreign key(srcid) references src(srcid)
);
