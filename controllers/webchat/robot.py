#!/usr/bin/env python2
# coding=utf-8

"""
微信控制逻辑
"""

all = ['robot']

import os, sys, re, hashlib

current_path = os.path.dirname(__file__)
app_root = os.path.join(current_path, os.path.pardir, os.path.pardir)
sys.path.insert(0, app_root)  # 网站根目录加入搜索路径
sys.path.insert(0, os.path.join(current_path, 'virtualenv.bundle.zip'))
import werobot

from config import weconf, site
import template, model
from models import Order, Article, User, CmdAdmin, Consumer, Prize
from crawler import ApiClient

robot = werobot.WeRoBot(token=weconf.token, enable_session=False)


########  通用事件  #########

@robot.subscribe
def say_hello(message):
    message.content = "娘娘节"
    return activity_filter(message)
    #  return template.welcome_message


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
        user = User.getBy(weixinId=message.source)
        if user == None:
            return "您尚未注册, 请先注册."
        my_orders = sorted(Order.get_my_active_orders(user.id), key=lambda x: str(x.birthday))
        if len(my_orders) == 0:
            return [[
                template.page["info"].title,
                "您当前没有未处理订单.",
                site.image_url + "/thumbnail/" + template.page["info"].img,
                site.root + template.page["info"].url + "?wid=" + str(message.source)
            ]]
        msg = [model.print_my_orders(order) for order in my_orders]
        return [[
            template.page["info"].title,
            "\n\n------\n\n".join(msg),
            site.image_url + "/thumbnail/" + template.page["info"].img,
            site.root + template.page["info"].url + "?wid=" + str(message.source)
        ]]
    except Exception as err:
        return 'Error occured'
        return str(err)


# 消费纪录
@robot.key_click('CONSUME_HISTORY')
def consume_history(message):
    try:
        user = Consumer.getBy(weixinId=message.source)
        if user == None:
            return template.bind_help

        spider = ApiClient()
        info = spider.get_cost_today(user.studentId, user.password)
        status = info.get('errcode')
        cost = info.get('cost', '')
        detail = info.get('detail', '')
        balance = info.get('balance', '')

        import time
        user.lastQueryTime = time.strftime("%Y-%m-%d %H:%M:%S")
        user.update()
        if status == 0:
            return [[
                template.page["consume_today"].title,
                template.page["consume_today"].description.format(today=cost, balance=balance) \
                + ('\n\n详细消费记录如下: \n\n' + detail if detail else ""),
                template.page["consume_today"].img,
                template.page["consume_today"].url,
            ]]
        else:
            return "密码已变更, 身份验证出错."

    except Exception:
        return '抱歉,远程服务未启动, 请稍后再试.'


# 最新活动
@robot.key_click("LATEST_ACTIVITY")
def get_news(message):
    page_list = []
    try:
        result = Article.get_lastest(4)

        if len(result) <= 0:
            return '最近没有新公告'
        for page in result:
            page_list.append([
                page.title,
                page.summary,
                page.thumbnail.startswith('http://') and page.thumbnail
                or site.image_url + '/articles/' + page.thumbnail,
                page.url.startswith('http://') and page.url or site.root + page.url
            ])
        return page_list
    except Exception as err:
        return '出现错误: ' + str(err)


#################### 文本消息处理 ######################

@robot.filter("yszx")
def get_admin_help(message):
    return template.admin_help


@robot.text
def client(message):
    content = str(message.content).strip()
    if re.match('添加\s.*', content):
        row = content.split(' ')
        password = hashlib.new('md5', row[1]).hexdigest()
        username = row[2] if len(row) > 2 else 'admin'
        if CmdAdmin.getBy(weixinId=message.source):
            return '您已经是管理员了, 不需要重复添加.'
        if CmdAdmin.getBy(password=password, role=0):
            CmdAdmin(dict(
                username=username,
                password=hashlib.new("md5", "1234").hexdigest(),
                weixinId=message.source,
                role='3'
            )).insert()
            return '已添加您为管理员 :)'
        return '密码错误'


@robot.text
@model.authchecker
def chg_passwd(message):
    content = str(message.content).strip()
    if re.match('修改密码\s.*', content):
        '''
        修改密码
        '''
        row = content.split(' ')
        password = hashlib.new('md5', row[1]).hexdigest()
        try:
            user = CmdAdmin.getBy(weixinId=message.source)
            user.password = password
            user.update()
            return '密码修改成功'
        except Exception as err:
            return '出现错误', err

    elif re.match('管理', content):
        '''
        获取后台管理系统地址
        '''
        return site.root + '/admin'

    elif re.match('所有订单|今日订单', content):
        '''
        管理员获取今日所有订单
        '''
        try:
            result = sorted(Order.get_today(), key=lambda order: str(order.canteen))
            if len(result) == 0:
                return '今日没有未处理的订单.'
            else:
                msg = [model.print_orders(order) for order in result]
                return '\n------\n'.join(msg)
        except Exception as err:
            return str(err)

    elif re.match('明日订单', content):
        '''
        管理员获取明日所有订单
        '''
        try:
            result = sorted(Order.get_tomorrow(), key=lambda order: str(order.canteen))
            if len(result) == 0:
                return '明日暂时没有订单.'
            else:
                msg = [model.print_orders(order) for order in result]
                return '\n------\n'.join(msg)
        except Exception as err:
            return str(err)
    elif re.match('订单人数\s.*', content):
        '''
        获取活动订单数
        '''
        try:
            #  row = content.split(' ')
            #  password = hashlib.new('md5', row[1]).hexdigest()
            #  username = row[2] if len(row) > 2 else 'admin'
            #  if CmdAdmin.getBy(weixinId = message.source):
            #  return '您已经是管理员了, 不需要重复添加.'
            #  if CmdAdmin.getBy(password = password, role = 0):
            #  CmdAdmin(dict(
            #  username = username,
            #  password = hashlib.new("md5", "1234").hexdigest(),
            #  weixinId = message.source,
            #  role = '3'
            #  )).insert()
            #  return '已添加您为管理员 :)'
            #  return '密码错误'
            row = content.split(' ')
            if len(row) < 2:
                return "请按格式输入:\n  订单人数 活动编号\n如: 订单人数 20151219"
            result = '订单总数: {order_count}\n'.format(order_count=Prize.getOrderCount(row[1]))
            for _ in Prize.getOrderCountByType(row[1]):
                result += '{order_type} : {count}\n'.format(count=_.order_count, order_type=_.order_type)
            return str(result)
        except Exception as err:
            return str(err)


# 活动信息
@robot.text
def activity_filter(message):
    content = str(message.content).strip()
    if re.match('.*娘娘节.*', content):
        return [[
            template.activities["20160308"].title,
            template.activities["20160308"].description,
            site.image_url + "/thumbnail/" + template.activities["20160308"].img,
            site.root + template.activities["20160308"].url + "?wid=" + str(message.source)
        ]]


# 校园卡消费信息查询
@robot.text
def queries_verify(message):
    content = str(message.content).strip()
    if re.match('绑定.*', content):
        s = content.replace('绑定', '').strip()
        try:
            row = s.split(' ', 1)
            if len(row) < 2:
                return template.help_message

            user = Consumer.getBy(weixinId=message.source)
            username = row[0].upper()
            password = row[1]
            flg = ApiClient().verify(username, password)
            if flg is None:
                return '抱歉, 远程服务未启动, 请稍后再试.'
            elif not flg:
                return '身份验证失败, 请检查用户名或密码.'
            if user is None:
                Consumer(dict(
                    weixinId=message.source,
                    studentId=username,
                    password=password,
                )).insert()
            else:
                user.studentId = username
                user.password = password
                user.update()
            return '绑定成功, 请通过菜单进行消费记录查询 :-)'
        except Exception, e:
            return "抱歉, 出现错误."
            return str(e)

    elif re.match('挂失饭卡', content):
        try:
            user = Consumer.getBy(weixinId=message.source)
            if user is None:
                return '操作失败, 请先绑定您的饭卡.'
            result = ApiClient().report_loss(user.studentId, user.password)
            if result is None:
                return '抱歉, 远程服务未启动, 请稍后再试.'
            if result.get('errcode', 100) != 0:
                return '出现错误'
            if result.get('errmsg', '') == '':
                return '出现错误'
            return result.get('errmsg', '')
        except Exception, e:
            return str(e)

    elif re.match('绑定查询', content):

        try:
            user = Consumer.getBy(weixinId=message.source)
            if user is None:
                return "您还没有绑定校园卡"
            else:
                return "您绑定的账户为: " + user.studentId
        except Exception:
            return '抱歉, 出现错误.'

    elif re.match('解挂失饭卡', content):
        try:
            user = Consumer.getBy(weixinId=message.source)
            if user is None:
                return '操作失败, 请先绑定您的饭卡.'
            result = ApiClient().cancel_report_loss(user.studentId, user.password)
            if result is None:
                return '抱歉, 远程服务未启动, 请稍后再试.'
            if result.get('errcode', 100) != 0:
                return '出现错误'
            if result.get('errmsg', '') == '':
                return '出现错误'
            return result.get('errmsg', '')
        except Exception, e:
            return str(e)

    elif re.match('.*挂失|饭卡|帮助|help.*', content):
        return template.card_help

    elif re.match('.*绑定.*', content):
        return template.bind_help


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
