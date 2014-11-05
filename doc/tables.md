数据表规划
---

系统数据表介绍

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



4. foodcenter_students



5. foodcenter_users



6. foodcenter_canteens


7. foodcenter_packages


8. foodcenter_cmd_admin

    微信管理账号


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


