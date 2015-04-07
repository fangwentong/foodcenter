#!/usr/bin/env python
#coding=utf-8

import web

class Session(web.session.Session):
    def __init__(self, app, store, initializer=None):
        web.session.Session.__init__(self, app, store, initializer)

    def expired(self):
        """Called when an expired session is atime
        """
        self._killed = True
        self._save()
        raise web.seeother("")