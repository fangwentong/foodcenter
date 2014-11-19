#!/usr/bin/env python2
#coding=utf-8

import web
import sys, os

from config.urls import urls
from config.setting import db
import models.home

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

app = web.application(urls, globals())
app.notfound = models.home.notfound

# Session
store = web.session.DBStore(db, 'foodcenter_sessions')
session = web.session.Session(app, store, initializer={'logged':False})
web.config._session = session

if __name__ == "__main__":
    if 'SERVER_SOFTWARE' in os.environ:
        import sae
        sae.create_wsgi_app(app.wsgifunc())
    else:
        app.run()
