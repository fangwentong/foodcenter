#!/usr/bin/env python
# coding=utf-8

import web

web.config.session_parameters = web.utils.storage({
    'cookie_name': 'webpy_session_id',
    'cookie_domain': None,
    'cookie_path': None,
    'timeout': 86400,  # 24 * 60 * 60, # 24 hours in seconds
    'ignore_expiry': True,
    'ignore_change_ip': True,
    'secret_key': 'fLjUfxqXtfNoIldA0A0J',
    'expired_message': 'Session expired',
    'httponly': True,
    'secure': False
})

class Session(web.session.Session):
    def __init__(self, app, store, initializer=None):
        super(Session, self).__init__(app, store, initializer)

    def expired(self):
        """
        Called when an expired session is atime
        重写session失效处理，取代默认行为
        """
        self._killed = True
        self._save()
        raise web.seeother("")

    def _setcookie(self, session_id, expires='', **kw):
        cookie_name = self._config.cookie_name
        cookie_domain = self._config.cookie_domain
        cookie_path = self._config.cookie_path
        httponly = self._config.httponly
        secure = self._config.secure
        expires = web.config.session_parameters.get('timeout')
        web.setcookie(cookie_name, session_id, expires=expires, domain=cookie_domain, httponly=httponly, secure=secure,
                      path=cookie_path)
web.session.Session = Session