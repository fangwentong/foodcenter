#!/usr/bin/env python
# coding=utf-8

from orm import Model, StringField, TimeField


class Consumer(Model):
    """
    饮食中心注册用户
    """
    __table__ = 'hitfd_consumers'

    weixinId = StringField(primary_key=True, updatable=False, ddl='varchar(255)')  # 微信 OpenId
    studentId = StringField(ddl='varchar(64)')  # 学号
    password = StringField(ddl='varchar(100)')  # 密码
    addTime = TimeField(ddl='timestamp')  # 添加日期
    lastQueryTime = TimeField(ddl='datetime')  # 上次查询时间
