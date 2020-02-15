drop table if exists bookrequests;
create table bookrequests (
  id integer primary key autoincrement,
  title text not null,
  dt datetime not null,
  email text not null,
  UNIQUE(title,email)
);