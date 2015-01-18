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
           host = "127.0.0.1",
           port = 3307,
           dbn  = 'mysql',
           db   = 'fd',
           user = 'root',
           pw   = 'root'
    )

webchat = web.storage (
        token = "token",
        appID = "wxappID",
        appsecret = "12345afea"
        )
