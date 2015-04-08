create table foodcenter_sessions (
    session_id char(128) unique not null,
    atime timestamp not null default current_timestamp,
    data text
);
-- generating SQL for foodcenter_admins:
create table `foodcenter_admins` (
  `id` int(11) not null,
  `username` varchar(255) not null,
  `password` varchar(255) not null,
  `role` int(11) not null,
  `nickname` varchar(64) not null,
  `email` varchar(128) not null,
  primary key(`id`)
);
-- generating SQL for foodcenter_canteens:
create table `foodcenter_canteens` (
  `id` int(11) not null,
  `name` varchar(50) not null,
  `picture` varchar(100) not null,
  `desription` varchar(2000) not null,
  `location` int(5) not null,
  `address` varchar(255) not null,
  primary key(`id`)
);
-- generating SQL for foodcenter_cmd_admins:
create table `foodcenter_cmd_admins` (
  `id` int(11) not null,
  `username` varchar(255) not null,
  `password` varchar(255) not null,
  `weixinId` varchar(255) not null,
  `role` int(11) not null,
  primary key(`id`)
);
-- generating SQL for foodcenter_meals:
create table `foodcenter_meals` (
  `id` int(11) not null,
  `name` varchar(50) not null,
  `picture` varchar(200) not null,
  `description` varchar(1000) not null,
  `active` bool not null,
  `canteenId` int(7) not null,
  `clock` varchar(255) not null,
  `sex_condition` int(1) not null,
  primary key(`id`)
);
-- generating SQL for foodcenter_orders:
create table `foodcenter_orders` (
  `id` int(11) not null,
  `userId` int(11) not null,
  `canteenId` int(7) not null,
  `mealId` int(11) not null,
  `studentId` varchar(64) not null,
  `studentName` varchar(255) not null,
  `sex` varchar(10) not null,
  `birthday` date not null,
  `token` int(6) not null,
  `wish` varchar(1000) not null,
  `addTime` timestamp not null,
  `isActive` bool not null,
  primary key(`id`)
);
-- generating SQL for foodcenter_students:
create table `foodcenter_students` (
  `id` int(12) not null,
  `studentId` varchar(64) not null,
  `StudentName` varchar(255) not null,
  `sex` varchar(10) not null,
  `identity` varchar(20) not null,
  `add_year` year(4) not null,
  primary key(`id`)
);
-- generating SQL for foodcenter_users:
create table `foodcenter_users` (
  `id` int(11) not null,
  `studentId` varchar(64) not null,
  `studentName` varchar(255) not null,
  `sex` varchar(10) not null,
  `birthday` date not null,
  `phone` varchar(30) not null,
  `shortMessage` varchar(1000) not null,
  `avatar` varchar(255) not null,
  `weixinId` varchar(255) not null,
  `nickname` varchar(255) not null,
  `lastOrderTime` date not null,
  `addTime` timestamp not null,
  `isLock` boolean not null,
  primary key(`id`)
);