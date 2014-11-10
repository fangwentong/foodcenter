#!/usr/bin/env python2
#coding=utf-8

import os
import sys

import hashlib
import web
from config.setting import weconf

app_root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(app_root, 'virtualenv.bundle.zip'))
import werobot

TOKEN = weconf.token

app_robot = werobot.WeRoBot(token = TOKEN, enable_session = False)


if __name__ == '__main__':
    if 'SERVER_SOFTWARE' in os.environ:
        import sae
        application = sae.create_wsgi_app(app_robot.wsgi)
    else:
        app_robot.run()
