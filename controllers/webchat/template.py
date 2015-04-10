#!/usr/bin/env python
#coding=utf-8

__all__ =['welcome_message', 'help_message', 'consume_message']

import web


page = { "signup" : web.storage(
            title       = "订单注册",
            description = "注册帐号，即刻免费优享生日面; 生日餐品以餐厅实际供应为准!",
            img         = "/register.jpg",
            url         = "/order/signup"
            ),
        "add"    : web.storage(
            title       = "添加订单",
            description = "优享生日美味，分享欢乐心情！",
            img         = "/add.jpg",
            url         = "/order/add"
            ),
        "info"   : web.storage(
            title       = "我的订单",
            description = "点击尝鲜~",
            img         = "/info.jpg",
            url         = "/order/info"
            ) }


# 消费信息
consume_message = \
""" 您上月共消费 180.20 元, 超过全校 25% 的用户.

早餐期间消费 2 次, 午餐期间消费 9 次, 晚餐期间消费 10 次.

小贴士:
"午饭饱,晚饭好,早餐少不了", 每天都记得吃早餐哦~

--------
数据来源: 哈工大后勤集团
(仅统计您在哈工大饮食中心下属各食堂的消费情况)

--------
以上数据为测试数据, 并无真实来源 """

# 欢迎提示
welcome_message = \
""" 我肥来啦~~你真有眼光，关注吃很重要，做一个有爱的吃货！ """

# 帮助信息
help_message = \
""" 欢迎关注饮食中心微信平台, 请直接键入问题或者拨打86418706^_^ """

# 所有订单
orderinfo = \
"""套餐名: {}
领取地点: {}
领餐人: {}
学号: {}
生日: {}"""
