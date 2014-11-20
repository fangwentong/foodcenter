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
