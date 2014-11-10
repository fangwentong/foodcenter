-- 1. foodcenter_admins

CREATE TABLE IF NOT EXISTS `foodcenter_admins` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `password` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `role` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- 2. foodcenter_feedbacks

    CREATE TABLE IF NOT EXISTS `foodcenter_feedbacks` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
      `email` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
      `phone` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
      `content` varchar(2500) COLLATE utf8_unicode_ci DEFAULT NULL,
      `solved` int(1) DEFAULT '0',
      `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- 3. foodcenter_orders

CREATE TABLE IF NOT EXISTS `foodcenter_orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `canteen_id` int(11) NOT NULL,
  `package_id` int(11) NOT NULL,
  `location` int(1) NOT NULL,
  `description` varchar(1000) COLLATE utf8_unicode_ci DEFAULT NULL,
  `student_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `student_id` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `phone` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `sex` int(1) NOT NULL,
  `birthday` date NOT NULL,
  `token` int(4) NOT NULL,
  `wish` varchar(1000) COLLATE utf8_unicode_ci DEFAULT NULL,
  `addtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `active` int(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- 4. foodcenter_students

CREATE TABLE IF NOT EXISTS `foodcenter_students` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `student_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `sex` int(1) DEFAULT NULL,
  `identity` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `add_year` int(4) NOT NULL DEFAULT '2014',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


-- 5. foodcenter_users

CREATE TABLE IF NOT EXISTS `foodcenter_users` (
  `number` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `student_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sex` int(1) DEFAULT NULL,
  `birthday` date NOT NULL,
  `phone` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `short_message` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL,
  `avatar` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `weixinId` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `last_order_time` date NOT NULL,
  `add_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `lock` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- 6. foodcenter_canteens

CREATE TABLE IF NOT EXISTS `foodcenter_canteen` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `picture` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `description` varchar(2000) COLLATE utf8_unicode_ci DEFAULT NULL,
  `location` int(1) NOT NULL DEFAULT '1',
  `address` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- 7. foodcenter_meals

CREATE TABLE IF NOT EXISTS `foodcenter_meals` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `picture` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `description` varchar(1000) COLLATE utf8_unicode_ci DEFAULT NULL,
  `isactive` int(1) NOT NULL DEFAULT '0',
  `address` int(7) NOT NULL,
  `time` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `location` int(1) NOT NULL,
  `sex_condition` int(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


-- 8. foodcenter_cmd_admin

CREATE TABLE IF NOT EXISTS `foodcenter_cmd_admins` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `WeixinId` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;