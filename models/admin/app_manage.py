#!/usr/bin/env python2
#coding=utf-8

import web
import sys, os
from url import urls

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

management_app = web.application(urls, locals())
# management_app.notfound = models.home.notfound

if __name__ == "__main__":
    if 'SERVER_SOFTWARE' in os.environ:
        import sae
        sae.create_wsgi_app(management_app.wsgifunc())
    else:
        management_app.run()
