#!/usr/bin/env python2
#coding=utf-8

import web
import sys, os
import models.iweb

from config.urls import urls
from config.setting import db
import models.home

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

abspath = os.path.dirname(__file__)
if abspath == "":
    abspath = "."
sys.path.append(abspath)
os.chdir(abspath)

app = web.application(urls, globals(), autoreload=True)
app.notfound = models.home.notfound

# Session
if web.config.get('_session') is None:
    web.config.session_parameters['cookie_name'] = 'foodcenter_sid'
    web.config.session_parameters['secret_key'] = 'Jfadfsajk139wagistviwt2'
    store = web.session.DBStore(db, 'foodcenter_sessions')
    web.config._session = models.iweb.session.Session(app, store, initializer={'logged':False, 'role':'guest'})

if __name__ == "__main__":
    if 'SERVER_SOFTWARE' in os.environ:
        import sae
        sae.create_wsgi_app(app.wsgifunc())
    else:
        app.run()
