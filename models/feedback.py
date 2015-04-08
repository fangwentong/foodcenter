#!/usr/bin/env python
#coding=utf-8

from orm import Model, StringField, IntegerField, BooleanField, TimeField

class FeedBack(Model):
    """
    反馈
    """
    __table__ = 'foodcenter_feedbacks'

    id       = IntegerField(primary_key=True, ddl='int(11)', ai=True, updatable=False)
    name     = StringField(ddl='varchar(255)')                       # 用户名
    email    = StringField(ddl="varchar(128)")                       # 邮箱
    phone    = StringField(ddl='varchar(30)')                        # 电话
    content  = StringField(ddl='varchar(2500)')                      # 反馈内容
    solved   = BooleanField(default=False)                            # 是否解决
    addTime  = TimeField()                                           # 添加时间

