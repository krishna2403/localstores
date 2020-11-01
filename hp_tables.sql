drop schema if exists localFoods;
create schema if not exists localFoods;
use localfoods;

create table if not exists business_type (
	business_type_id int not null auto_increment,
    business_type_name varchar(500) not null,
    primary key (business_type_id)
);

create table if not exists businesses (
	business_id int not null auto_increment,
    business_name varchar(500) not null,
    manager_name varchar(500) not null,
    business_type_id int not null,
    business_pwd varchar(500) not null,
    primary key (business_id),
    foreign key (business_type_id)
    references business_type(business_type_id)
);

create table if not exists users (
	user_id int not null auto_increment,
    user_name varchar(500) not null,
    user_pwd varchar(500) not null,
    primary key (user_id)
);


-- use localfoods;
-- insert into business_type(business_type_id, business_type_name) values(1, 'food'), (2, 'food'), (3, 'food');
-- delete from business_type where business_type_id=3;
-- SELECT * FROM localfoods.users;