#!/usr/bin/env python
#coding=utf-8

"""
webpy 与 WeRobot 交互的中间层
"""

__all__ = ['WeixinHandler']

import os, sys
import web

app_root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(app_root, 'virtualenv.bundle.zip'))

from werobot.parser import parse_user_msg
from werobot.reply import create_reply
from robot import robot

class WeixinHandler():
    def __init__(self):
        self.data  = web.input(timestamp = "",
                nonce = "",
                signature = "",
                echostr = ""
                )
        timestamp = self.data.timestamp
        nonce = self.data.nonce
        signature = self.data.signature
        if not robot.check_signature(
            timestamp=timestamp,
            nonce=nonce,
            signature=signature
        ):
            raise web.Forbidden()

    def GET(self):
        return self.data.echostr

    def POST(self):
        body = web.data()
        message = parse_user_msg(body)
        reply = robot.get_reply(message)
        web.header('Content-Type', 'text/xml')
        return create_reply(reply, message=message)