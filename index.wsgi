#!/usr/bin/env python2
#coding=utf-8

import os
from app import app
import web

"""
此文件专用于服务器端部署
本地直接运行同目录下的app.py
"""

if 'SERVER_SOFTWARE' in os.environ:
    # sae部署
    import sae
    application = sae.create_wsgi_app(app.wsgifunc())
else:
    # Nginx with Fastcgi 部署
    os.environ["SCRIPT_NAME"] = ""
    os.environ["REAL_SCRIPT_NAME"] = ""
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()
