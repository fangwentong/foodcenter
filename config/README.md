配置文件介绍
---


处于安全性考虑，网站的部分配置不宜公开，这些配置项被加入到`secret.py`,
其配置样例有:

``` python
#coding=utf-8

import web
import sae.const
import os

if 'SERVER_SOFTWARE' in os.environ:
    db = web.database(
            host = sae.const.MYSQL_HOST,
            port = int(sae.const.MYSQL_PORT),
            dbn  = 'mysql',
            db   = sae.const.MYSQL_DB,
            user = sae.const.MYSQL_USER,
            pw   = sae.const.MYSQL_PASS
            )
else:
    db = web.database (
           host = HOST_ADRESS,
           port = PORT,
           dbn  = 'mysql',
           db   = DB_NAME,
           user = USER_NAME,
           pw   = PASSWORD
    )

webchat = web.storage (
        token = "token",
        appID = "wxappID",
        appsecret = "12345afea"
        )
```


