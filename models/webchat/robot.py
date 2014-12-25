#!/usr/bin/env python2
#coding=utf-8

"""

"""

all = ['robot']

import os
import sys

from config.setting import weconf
from config import setting
import basic

app_root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(app_root, 'virtualenv.bundle.zip'))
import werobot

TOKEN = weconf.token

robot = werobot.WeRoBot(token = TOKEN, enable_session = False)

# 控制逻辑

########### 订阅 / 退订事件 ####################
@robot.subscribe
def say_hello(message):
    return basic.welcome_message

@robot.unsubscribe
def unsubscri(message):
    pass

############## click 事件处理 ##################

# 订餐注册
@robot.key_click("SIGNUP")
def signup(message):
    return [[
        basic.page["signup"].title,
        basic.page["signup"].description,
        setting.image_url + "/thumbnail/" + basic.page["signup"].img,
        setting.site.root + basic.page["signup"].url + "?wid=" + str(message.source)
        ]]

# 添加订单
@robot.key_click("ADDORDER")
def add_order(message):
    return [[
        basic.page["add"].title,
        basic.page["add"].description,
        setting.image_url + "/thumbnail/" + basic.page["add"].img,
        setting.site.root + basic.page["add"].url + "?wid=" + str(message.source)
        ]]

# 我的订单
@robot.key_click("MYORDER")
def get_my_order(message):
    return [[
        basic.page["info"].title,
        basic.page["info"].description,
        setting.image_url + "/thumbnail/" + basic.page["info"].img,
        setting.site.root + basic.page["info"].url + "?wid=" + str(message.source)
        ]]

# 消费纪录
@robot.key_click("CONSUME_HISTORY")
def consume_history(message):
    # return "对不起,没有找到您的消费信息."
    return basic.consume_message

# 最新活动
@robot.key_click("LATEST_ACTIVITY")
def get_news(message):
    pass

#################### 文本消息处理 ######################

@robot.text
def reply_text(message):
    return basic.help_message

# @robot.handler
# def reply_others(message):
    # return basic.help_message

if __name__ == '__main__':
    if 'SERVER_SOFTWARE' in os.environ:
        import sae
        application = sae.create_wsgi_app(robot.wsgi)
    else:
        robot.run()

