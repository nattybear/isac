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

create view isacview as
	select ip.ip, country.countryname, attacktype.attacktypename, type.typename, src.srcname
	from "ip/attacktype/src"
	join ip on ip.ip="ip/attacktype/src".ip
	join country on ip.countrycode=country.countrycode
	join attacktype on "ip/attacktype/src".attacktypeid=attacktype.attacktypeid
	join type on attacktype.typeid=type.typeid
	join src on "ip/attacktype/src".srcid=src.srcid
	join level on type.levelid=level.levelid
	order by priority;
