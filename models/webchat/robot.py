#!/usr/bin/env python2
#coding=utf-8

"""

"""

all = ['robot']

import os
import sys

from config.setting import weconf
import basic

app_root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(app_root, 'virtualenv.bundle.zip'))
import werobot

TOKEN = weconf.token

robot = werobot.WeRoBot(token = TOKEN, enable_session = False)

# 控制逻辑

@robot.key_click("CONSUME_HISTORY")
def consume_history(message):
    # return "对不起,没有找到您的消费信息."
    return basic.consume_content

@robot.subscribe
def say_hello(message):
    return basic.hello_content

@robot.text
def reply_text(message):
    return basic.other_content

@robot.handler
def reply_others(message):
    return basic.other_content

if __name__ == '__main__':
    if 'SERVER_SOFTWARE' in os.environ:
        import sae
        application = sae.create_wsgi_app(robot.wsgi)
    else:
        robot.run()

