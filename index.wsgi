#!/usr/bin/env python2
# coding: utf-8

import os
from app import app

if 'SERVER_SOFTWARE' in os.environ:
    import sae
    application = sae.create_wsgi_app(app.wsgifunc())
else:
	app.run()
