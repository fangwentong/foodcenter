数据表规划
---

####系统数据表介绍

1. foodcenter_admins

    记录后台管理系统管理员信息，包括id, 用户名username,
    md5加密的密码password, 更加细化的角色标识role


    | Field    | Type         | Null | Key | Default | Extra          |
    |----------|--------------|------|-----|---------|----------------|
    | id       | int(11)      | NO   | PRI | NULL    | auto_increment |
    | username | varchar(255) | YES  |     | NULL    |                |
    | password | varchar(255) | YES  |     | NULL    |                |
    | role     | int(11)      | YES  |     | NULL    |                |

    ``` sql
    CREATE TABLE IF NOT EXISTS `foodcenter_admins` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `username` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
      `password` varchar(255) COLLATE utf8_bin DEFAULT NULL,
      `role` int(11) DEFAULT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
    ```

2. foodcenter_feedbacks

    记录用户反馈


    | Field   | Type          | Null | Key | Default           | Extra          |
    |:-------:|:-------------:|:----:|:---:|:-----------------:|:--------------:|
    | id      | int(11)       | NO   | PRI | NULL              | auto_increment |
    | name    | varchar(100)  | YES  |     | NULL              |                |
    | email   | varchar(100)  | YES  |     | NULL              |                |
    | phone   | varchar(30)   | YES  |     | NULL              |                |
    | content | varchar(2500) | YES  |     | NULL              |                |
    | solved  | int(1)        | YES  |     | NULL              |                |
    | addTime | timestamp     | YES  |     | CURRENT_TIMESTAMP |                |

    ``` sql
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
    ```

3. foodcenter_orders

    记录订单信息


    | Field        | Type          | Null | Key | Default           | Extra          |
    |:------------:|:-------------:|:----:|:---:|:-----------------:|:--------------:|
    | id           | int(11)       | NO   | PRI | NULL              | auto_increment |
    | user_id      | int(11)       | NO   |     | NULL              |                |
    | canteen_id   | int(11)       | NO   |     | NULL              |                |
    | package_id   | int(11)       | NO   |     | NULL              |                |
    | location     | int(1)        | NO   |     | NULL              |                |
    | description  | varchar(1000) | YES  |     | NULL              |                |
    | student_name | varchar(255)  | NO   |     | NULL              |                |
    | student_id   | varchar(64)   | NO   |     | NULL              |                |
    | phone        | varchar(64)   | NO   |     | NULL              |                |
    | sex          | int(1)        | NO   |     | NULL              |                |
    | birthday     | date          | NO   |     | NULL              |                |
    | token        | int(4)        | NO   |     | NULL              |                |
    | wish         | varchar(1000) | YES  |     | NULL              |                |
    | addtime      | timestamp     | NO   |     | CURRENT_TIMESTAMP |                |
    | active       | int(1)        | NO   |     | NULL              |                |

    ``` sql
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
    ```

4. foodcenter_students

    学生信息


    | Field        | Type         | Null | Key | Default | Extra          |
    |:------------:|:------------:|:----:|:---:|:-------:|:--------------:|
    | id           | int(11)      | NO   | PRI | NULL    | auto_increment |
    | student_id   | varchar(64)  | NO   |     | NULL    |                |
    | student_name | varchar(255) | NO   |     | NULL    |                |
    | sex          | int(1)       | YES  |     | NULL    |                |
    | identity     | varchar(255) | YES  |     | NULL    |                |
    | add_year     | int(4)       | NO   |     | 2014    |                |

    ``` sql
    CREATE TABLE IF NOT EXISTS `foodcenter_students` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `student_id` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
      `student_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
      `sex` int(1) DEFAULT NULL,
      `identity` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
      `add_year` int(4) NOT NULL DEFAULT '2014',
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
    ```


5. foodcenter_users

    已注册用户信息


    | Field           | Type         | Null | Key | Default           | Extra          |
    |:---------------:|:------------:|:----:|:---:|:-----------------:|:--------------:|
    | number          | int(11)      | NO   | PRI | NULL              | auto_increment |
    | student_id      | varchar(64)  | YES  |     | NULL              |                |
    | student_name    | varchar(255) | YES  |     | NULL              |                |
    | sex             | int(1)       | YES  |     | NULL              |                |
    | birthday        | date         | NO   |     | NULL              |                |
    | phone           | varchar(64)  | YES  |     | NULL              |                |
    | short_message   | varchar(500) | YES  |     | NULL              |                |
    | avatar          | varchar(255) | YES  |     | NULL              |                |
    | openId          | varchar(255) | YES  |     | NULL              |                |
    | nickname        | varchar(255) | YES  |     | NULL              |                |
    | last_order_time | date         | NO   |     | NULL              |                |
    | addTime         | timestamp    | NO   |     | CURRENT_TIMESTAMP |                |
    | lock            | int(1)       | NO   |     | 0                 |                |

    ``` sql
    CREATE TABLE IF NOT EXISTS `foodcenter_users` (
      `number` int(11) NOT NULL AUTO_INCREMENT,
      `student_id` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
      `student_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
      `sex` int(1) DEFAULT NULL,
      `birthday` date NOT NULL,
      `phone` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
      `short_message` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL,
      `avatar` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
      `weixinId` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
      `nickname` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
      `last_order_time` date NOT NULL,
      `add_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
      `lock` int(1) NOT NULL DEFAULT '0',
      PRIMARY KEY (`number`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
    ```

6. foodcenter_canteens

    餐厅表


    | Field       | Type          | Null | Key | Default | Extra          |
    |:-----------:|:-------------:|:----:|:---:|:-------:|:--------------:|
    | cid         | int(11)       | NO   | PRI | NULL    | auto_increment |
    | name        | varchar(50)   | NO   |     | NULL    |                |
    | picture     | varchar(100)  | YES  |     | NULL    |                |
    | description | varchar(2000) | YES  |     | NULL    |                |
    | location    | int(1)        | NO   |     | 1       |                |
    | address     | varchar(255)  | YES  |     | NULL    |                |

    ``` sql
    CREATE TABLE IF NOT EXISTS `foodcenter_canteen` (
      `cid` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
      `picture` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
      `description` varchar(2000) COLLATE utf8_unicode_ci DEFAULT NULL,
      `location` int(1) NOT NULL DEFAULT '1',
      `address` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
      PRIMARY KEY (`cid`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
    ```

7. foodcenter_meals

    生日餐供应表


    | Field         | Type          | Null | Key | Default | Extra          |
    +---------------+---------------+------+-----+---------+----------------+
    | id            | int(11)       | NO   | PRI | NULL    | auto_increment |
    | name          | varchar(50)   | NO   |     | NULL    |                |
    | picture       | varchar(100)  | YES  |     | NULL    |                |
    | description   | varchar(1000) | YES  |     | NULL    |                |
    | isactive      | int(1)        | NO   |     | 0       |                |
    | address       | int(7)        | NO   |     | NULL    |                |
    | time          | varchar(255)  | NO   |     | NULL    |                |
    | location      | int(1)        | NO   |     | NULL    |                |
    | sex_condition | int(1)        | NO   |     | NULL    |                |

    ``` sql
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
    ```



8. foodcenter_cmd_admin

    微信端管理账号


    | Field    | Type         | Null | Key | Default | Extra          |
    |:--------:|:------------:|:----:|:---:|:-------:|:--------------:|
    | id       | int(11)      | NO   | PRI | NULL    | auto_increment |
    | username | varchar(255) | YES  |     | NULL    |                |
    | password | varchar(255) | YES  |     | NULL    |                |
    | weixinId | varchar(255) | NO   |     |         |                |


    ``` sql
    CREATE TABLE IF NOT EXISTS `foodcenter_cmd_admins` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
      `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
      `WeixinId` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '',
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    ```

---

9. foodcenter


