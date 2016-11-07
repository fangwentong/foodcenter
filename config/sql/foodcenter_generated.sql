create database if not exists fd;
use fd;
create table if not exists hitfd_sessions (
    `session_id` char(128) unique not null,
    `atime` timestamp not null default current_timestamp,
    `data` text,
     primary key(`session_id`)
);
-- generating SQL for hitfd_admins:
create table if not exists `hitfd_admins` (
  `id` int(11) not null auto_increment COMMENT '',
  `username` varchar(255) not null COMMENT '',
  `password` varchar(255) not null COMMENT '',
  `role` int(11) not null COMMENT '',
  `nickname` varchar(64) not null COMMENT '',
  `email` varchar(128) not null COMMENT '',
  primary key(`id`)
);
-- generating SQL for hitfd_articles:
create table if not exists `hitfd_articles` (
  `id` int(15) not null auto_increment COMMENT '',
  `title` varchar(1000) not null COMMENT '',
  `thumbnail` varchar(1000) not null COMMENT '',
  `url` varchar(1000) not null COMMENT '',
  `lastModify` timestamp not null COMMENT '',
  `postTime` datetime not null COMMENT '',
  `isDraft` boolean not null COMMENT '',
  `summary` varchar(512) not null COMMENT '',
  `body` varchar(10000) not null COMMENT '',
  `visitors` varchar(12) not null COMMENT '',
  primary key(`id`)
);
-- generating SQL for hitfd_canteens:
create table if not exists `hitfd_canteens` (
  `id` int(11) not null auto_increment COMMENT '',
  `name` varchar(50) not null COMMENT '',
  `picture` varchar(100) not null COMMENT '',
  `description` varchar(2000) not null COMMENT '',
  `location` int(5) not null COMMENT '',
  `address` varchar(255) not null COMMENT '',
  primary key(`id`)
);
-- generating SQL for hitfd_cmd_admins:
create table if not exists `hitfd_cmd_admins` (
  `id` int(11) not null auto_increment COMMENT '',
  `username` varchar(255) not null COMMENT '',
  `password` varchar(255) not null COMMENT '',
  `weixinId` varchar(255) not null COMMENT '',
  `role` int(11) not null COMMENT '',
  primary key(`id`)
);
-- generating SQL for hitfd_feedbacks:
create table if not exists `hitfd_feedbacks` (
  `id` int(11) not null auto_increment COMMENT '',
  `name` varchar(255) not null COMMENT '',
  `email` varchar(128) not null COMMENT '',
  `phone` varchar(30) not null COMMENT '',
  `content` varchar(2500) not null COMMENT '',
  `solved` boolean not null COMMENT '',
  `addTime` timestamp not null COMMENT '',
  primary key(`id`)
);
-- generating SQL for hitfd_meals:
create table if not exists `hitfd_meals` (
  `id` int(11) not null auto_increment COMMENT '',
  `name` varchar(50) not null COMMENT '',
  `picture` varchar(200) not null COMMENT '',
  `description` varchar(1000) not null COMMENT '',
  `active` boolean not null COMMENT '',
  `canteenId` int(7) not null COMMENT '',
  `clock` varchar(255) not null COMMENT '',
  `sex_condition` int(1) not null COMMENT '',
  primary key(`id`)
);
-- generating SQL for hitfd_orders:
create table if not exists `hitfd_orders` (
  `id` int(11) not null auto_increment COMMENT '',
  `userId` int(11) not null COMMENT '',
  `canteenId` int(7) not null COMMENT '',
  `mealId` int(11) not null COMMENT '',
  `studentId` varchar(64) not null COMMENT '',
  `studentName` varchar(255) not null COMMENT '',
  `phone` varchar(30) not null COMMENT '',
  `sex` varchar(10) not null COMMENT '',
  `birthday` date not null COMMENT '',
  `token` int(6) not null COMMENT '',
  `wish` varchar(1000) not null COMMENT '',
  `addTime` timestamp not null COMMENT '',
  `isActive` boolean not null COMMENT '',
  primary key(`id`)
);
-- generating SQL for hitfd_students:
create table if not exists `hitfd_students` (
  `id` int(12) not null auto_increment COMMENT '',
  `studentId` varchar(64) not null COMMENT '',
  `studentName` varchar(255) not null COMMENT '',
  `sex` varchar(10) not null COMMENT '',
  `identity` varchar(20) not null COMMENT '',
  `add_year` year(4) not null COMMENT '',
  primary key(`id`)
);
-- generating SQL for hitfd_users:
create table if not exists `hitfd_users` (
  `id` int(11) not null auto_increment COMMENT '',
  `studentId` varchar(64) not null COMMENT '',
  `studentName` varchar(255) not null COMMENT '',
  `sex` varchar(10) not null COMMENT '',
  `birthday` date not null COMMENT '',
  `phone` varchar(30) not null COMMENT '',
  `shortMessage` varchar(1000) not null COMMENT '',
  `avatar` varchar(255) not null COMMENT '',
  `weixinId` varchar(255) not null COMMENT '',
  `nickname` varchar(255) not null COMMENT '',
  `lastOrderTime` date not null COMMENT '',
  `addTime` timestamp not null COMMENT '',
  `isLock` boolean not null COMMENT '',
  primary key(`id`)
);
-- generating SQL for hitfd_consumers:
create table if not exists `hitfd_consumers` (
  `weixinId` varchar(255) not null COMMENT '',
  `studentId` varchar(64) not null COMMENT '',
  `password` varchar(100) not null COMMENT '',
  `addTime` timestamp not null COMMENT '',
  `lastQueryTime` datetime not null COMMENT '',
  primary key(`weixinId`)
);