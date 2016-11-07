#!/usr/bin/env python
# coding=utf-8

from orm import Model, StringField, TimeField, IntegerField
from orm import db


class Prize(Model):
    """
    饮食中心注册用户
    """
    __table__ = 'hitfd_prizes'

    id = IntegerField(primary_key=True, updatable=False, ai=True, ddl='int(12)')
    weixinId = StringField(ddl='varchar(255)')  # 微信 OpenId
    order_number = StringField(ddl='varchar(50)')
    order_type = IntegerField(ddl='int(11)')  # 订单类型
    activity_number = StringField(ddl="varchar(255)")  # 活动编号
    addTime = TimeField(ddl='timestamp')  # 添加日期
    phone = StringField(ddl='varchar(15)')
    cookie = StringField(ddl='varchar(250)')
    is_used = IntegerField(ddl="tinyint(1)")  # 是否使用 0: 未使用, 1: 已使用

    @classmethod
    def getMaxNum(cls, key='order_number'):
        result = list(db.query('select max({}) as max_value from hitfd_prizes'.format(key)))[0].max_value
        if result is None or long(result) < 4000:
            return 4000
        else:
            return long(result)

    '''
    获取某次活动的订单总数
    '''

    @classmethod
    def getOrderCount(cls, activity_number, key='order_number'):
        result = list(db.query(
            'select count(*) as order_count from hitfd_prizes where activity_number = {activity_number}'.format(
                key=key,
                activity_number=activity_number,
            )))
        if result == None or result[0] == None:
            return 0
        return result[0].order_count

    '''
    获取某次活动的订单 -- 根据餐品种类统计
    '''

    @classmethod
    def getOrderCountByType(cls, activity_number, key='order_number'):
        result = list(db.query(
            'select count(*) as order_count, order_type from hitfd_prizes where activity_number = {activity_number} group by order_type'.format(
                key=key,
                activity_number=activity_number,
            )))
        return result

    '''
    获取某次活动的当前可用订单号
    '''

    @classmethod
    def getOrderNumber(cls, activity_number, start, key='order_number'):
        result = list(db.query(
            'select max({key}) as max_value from hitfd_prizes where activity_number = {activity_number}'.format(
                key=key,
                activity_number=activity_number,
            )))
        if result is None or result[0] is None or result[0].max_value is None:
            return start
        return int(result[0].max_value) + 1
