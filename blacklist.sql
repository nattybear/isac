create table ip (
	ip text primary key
);

create table attacktype (
	attacktypeid integer primary key autoincrement,
	attacktypename text unique,
	typeid integer,
	foreign key(typeid) references type(typeid)
);

create table type (
	typeid integer primary key autoincrement,
	typename text unique,
	levelid integer,
	foreign key(levelid) references level(levelid)
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
	unique(day, ip, attacktypeid, srcid),
	foreign key(ip) references ip(ip),
	foreign key(attacktypeid) references attacktype(attacktypeid),
	foreign key(srcid) references src(srcid)
);

create table country (
	countrycode text primary key,
	countryname text unique
);
