#!/usr/bin/env python
#coding=utf-8


from orm import Model, StringField, IntegerField, DateField, TimeField, BooleanField

class Order(Model):
    """
    订单
    """
    __table__ = 'foodcenter_orders'

    id          = IntegerField(primary_key=True, nullable=False, ddl='int(11)')
    userId      = IntegerField(ddl='int(11)')        # 订餐人id
    canteenId   = IntegerField(ddl='int(7)')         # 就餐餐厅
    mealId      = IntegerField('int(11)')            # 套餐
    studentId   = StringField(ddl="varchar(64)")     # 就餐人学号
    studentName = StringField(ddl='varchar(255)')    # 就餐人姓名
    sex         = StringField(ddl='varchar(10)')     # 性别
    birthday    = DateField(ddl='date')              # 生日
    token       = IntegerField(ddl='int(6)')         # 6位 Token
    wish        = StringField(ddl='varchar(1000)')   # 生日祝福
    addTime     = TimeField()                        # 订单添加时间
    isActive    = BooleanField(default=True)         # 是否有效

