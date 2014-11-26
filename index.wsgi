#!/usr/bin/env python2
#coding=utf-8

import os
from app import app
import web

"""
本文件专用于在服务器上部署
本地直接运行同目录下的app.py
"""

if 'SERVER_SOFTWARE' in os.environ:
    # sae部署
    import sae
    application = sae.create_wsgi_app(app.wsgifunc())
else:
    # Nginx + Fastcgi 部署
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()
