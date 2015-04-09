#!/usr/bin/env python
#coding=utf-8

from orm import Model, StringField, IntegerField, DateField, TimeField, BooleanField

class User(Model):
    """
    饮食中心注册用户
    """
    __table__ = 'foodcenter_users'

    id            = IntegerField(primary_key=True, updatable=False, ai=True, ddl='int(11)')
    studentId     = StringField(ddl="varchar(64)", updatable=False)    # 学号
    studentName   = StringField(ddl='varchar(255)', updatable=False)   # 姓名
    sex           = StringField(ddl='varchar(10)')    # 性别
    birthday      = DateField()                       # 生日
    phone         = StringField(ddl='varchar(30)')    # 电话
    shortMessage  = StringField(ddl='varchar(1000)')  # 签名
    avatar        = StringField(ddl='varchar(255)')   # 头像
    weixinId      = StringField(ddl='varchar(255)')   # 微信 OpenId
    nickname      = StringField(ddl='varchar(255)')   # 昵称
    lastOrderTime = StringField(ddl='date')           # 上一订单时间
    addTime       = TimeField(ddl='timestamp')        # 注册日期
    isLock        = BooleanField(ddl='boolean')       # 是否被锁定

