#!/usr/bin/env python
#coding=utf-8

import web

class Session(web.session.Session):
    def __init__(self, app, store, initializer=None):
        web.session.Session.__init__(self, app, store, initializer)

    def expired(self):
        """
        Called when an expired session is atime
        重写session失效处理，取代默认行为
        """
        self._killed = True
        self._save()
        raise web.seeother("")
