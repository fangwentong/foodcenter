#!/usr/bin/env python2
#coding=utf-8

"""

"""

all = ['robot']

import os, sys
import time

from config.setting import weconf
from config import setting
import basic

render = setting.render
db = setting.db

app_root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(app_root, 'virtualenv.bundle.zip'))
import werobot

robot = werobot.WeRoBot(token = weconf.token, enable_session = False)

# 控制逻辑

############## Models ##################
def get_package_name(package_id):
    try:
        sql = "SELECT * FROM foodcenter_meals WHERE id=$id"
        result = list(db.query(sql, vars={'id' : str(package_id)}))
        if len(result) > 0:
            return result[0].name
        else:
            return "没有找到匹配的套餐"
    except Exception as err:
        return "出现错误: " + str(err)

def get_canteen_name(canteen_id):
    try:
        sql = "SELECT * FROM foodcenter_canteen WHERE cid=$cid"
        result = list(db.query(sql, vars={'cid' : canteen_id}))
        if len(result) > 0:
            return result[0].name
        else:
            return "没有找到匹配的餐厅"
    except Exception as err:
        return "出现错误: " + str(err)

def authchecker(func):
    """管理员权限验证"""
    def _authchecker(message):
        try:
            sql = "SELECT * FROM foodcenter_cmd_admins WHERE WeixinId=$wx_id"
            result = list(db.query(sql, vars={'wx_id' : message.source}))
            if len(result) <= 0:
                return basic.help_message
            else:
                return func(message)

        except Exception as err:
            return "出现错误: " + str(err)
    return _authchecker

########################################
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
                setting.image_url + "/articles/" + page.thumbnail,
                setting.site.root + page.url
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
    return setting.site.root + "/admin"


# 默认Handler
@robot.handler
def reply_others(message):
    return basic.help_message


if __name__ == '__main__':
    if 'SERVER_SOFTWARE' in os.environ:
        import sae
        application = sae.create_wsgi_app(robot.wsgi)
    else:
        robot.run()

