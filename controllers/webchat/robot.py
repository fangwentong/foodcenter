#!/usr/bin/env python2
#coding=utf-8

"""
微信控制逻辑
"""

all = ['robot']

import os, sys
import time

current_path = os.path.dirname(__file__)
app_root = os.path.join(current_path, os.path.pardir, os.path.pardir)
sys.path.insert(0, app_root)             # 网站根目录加入搜索路径
sys.path.insert(0, os.path.join(current_path, 'virtualenv.bundle.zip'))
import werobot

from config import weconf
from config import db, site
import template

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
        site.site.root + template.page["signup"].url + "?wid=" + str(message.source)
        ]]

# 添加订单
@robot.key_click("ADDORDER")
def add_order(message):
    return [[
        template.page["add"].title,
        template.page["add"].description,
        site.image_url + "/thumbnail/" + template.page["add"].img,
        site.site.root + template.page["add"].url + "?wid=" + str(message.source)
        ]]

# 我的订单
@robot.key_click("MYORDER")
def get_my_order(message):
    return [[
        template.page["info"].title,
        template.page["info"].description,
        site.image_url + "/thumbnail/" + template.page["info"].img,
        site.site.root + template.page["info"].url + "?wid=" + str(message.source)
        ]]

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
        sql = "SELECT * from foodcenter_articles WHERE is_active=$active"
        result = list(db.query(sql, vars={'active' : '1'}))

        if len(result) <= 0:
            return "最近没有新公告"
        for page in result:
            page_list.append([
                page.title,
                page.summary,
                site.image_url + "/articles/" + page.thumbnail,
                site.site.root + page.url
                ])
        return page_list
    except Exception as err:
        return "出现错误: " + err

#################### 文本消息处理 ######################

@robot.filter("所有订单")
@authchecker
def get_all_order(message):
    try:
        TODAY = time.strftime('%Y-%m-%d')
        sql = "SELECT * FROM foodcenter_orders WHERE birthday=$birthday AND active=$active"
        result = list(db.query(sql, vars={'birthday' : TODAY, 'active' : '1'}))
        if len(result) == 0:
            return TODAY
            return "今日没有未处理的订单."
        else:
            msg = "#套餐名   #领取地址  #领餐人 #学号 #领餐日期 \n"
            for order in result:
                msg += get_package_name(order.package_id) + "  " + get_canteen_name(order.canteen_id)\
                        + "  " + order.student_name + "  " + order.student_id + "  " + str(order.birthday) + "\n\n"
            return msg
    except Exception as err:
        return str(err)

@robot.filter("管理")
@authchecker
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
