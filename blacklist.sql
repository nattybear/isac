begin transaction;
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
rollback;
