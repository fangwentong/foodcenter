#!/usr/bin/env python2
#coding=utf-8

"""
微信控制逻辑
"""

all = ['robot']

import os, sys

current_path = os.path.dirname(__file__)
app_root = os.path.join(current_path, os.path.pardir, os.path.pardir)
sys.path.insert(0, app_root)             # 网站根目录加入搜索路径
sys.path.insert(0, os.path.join(current_path, 'virtualenv.bundle.zip'))
import werobot

from config import weconf
from config import site
import template
from models import Order, Article, User
import model

robot = werobot.WeRoBot(token = weconf.token, enable_session = False)


########  通用事件  #########

@robot.subscribe
def say_hello(message):
    return template.welcome_message

@robot.unsubscribe
def unsubscribe(message):
    pass


# 订餐注册
@robot.key_click("SIGNUP")
def signup(message):
    return [[
        template.page["signup"].title,
        template.page["signup"].description,
        site.image_url + "/thumbnail/" + template.page["signup"].img,
        site.root + template.page["signup"].url + "?wid=" + str(message.source)
        ]]


# 添加订单
@robot.key_click("ADDORDER")
def add_order(message):
    return [[
        template.page["add"].title,
        template.page["add"].description,
        site.image_url + "/thumbnail/" + template.page["add"].img,
        site.root + template.page["add"].url + "?wid=" + str(message.source)
        ]]


# 我的订单
@robot.key_click("MYORDER")
def get_my_order(message):
    try:
        user = User.getBy(weixinId = message.source)
        if user == None:
            return "您尚未注册, 请先注册."
        my_orders = Order.get_my_active_orders(user.id)
        if len(my_orders) == 0:
            return "您当前没有未处理订单."
        msg = [model.print_my_orders(order) for order in my_orders]
        return "\n------\n".join(msg)
    except Exception as err:
        return str(err)


# 消费纪录
@robot.key_click("CONSUME_HISTORY")
def consume_history(message):
    # return "对不起,没有找到您的消费信息."
    return template.consume_message


# 最新活动
@robot.key_click("LATEST_ACTIVITY")
def get_news(message):
    page_list = []
    try:
        result = Article.get_lastest(5)

        if len(result) <= 0:
            return "最近没有新公告"
        for page in result:
            page_list.append([
                page.title,
                page.summary,
                site.image_url + "/articles/" + page.thumbnail,
                site.root + page.url
                ])
        return page_list
    except Exception as err:
        return "出现错误: " + err


#################### 文本消息处理 ######################

# 所有订单 @cmdadmin
@robot.filter("所有订单")
@model.authchecker
def get_all_order(message):
    try:
        result = Order.get_today()
        if len(result) == 0:
            return "今日没有未处理的订单."
        else:
            msg = [model.print_orders(order) for order in result]
            return "\n------\n".join(msg)
    except Exception as err:
        return str(err)


# 后台管理系统地址 @cmdadmin
@robot.filter("管理")
@model.authchecker
def get_admin_entrance(message):
    return site.root + "/admin"


# 默认Handler
@robot.handler
def reply_others(message):
    return template.help_message

if __name__ == '__main__':
    if 'SERVER_SOFTWARE' in os.environ:
        import sae
        application = sae.create_wsgi_app(robot.wsgi)
    else:
        robot.run()
