drop table if exists users;

create table users(
  user_name varchar(100) not null,
  email varchar(200),
  id int auto_increment primary key not null
) engine=InnoDB;

