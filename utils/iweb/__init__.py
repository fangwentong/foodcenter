#!/usr/bin/env python
# encoding: utf-8

# Override some web.py class
all = ["web"]

import web
try:
    import session.Session
    web.session.Session = session.Session
except ImportError:
    pass
