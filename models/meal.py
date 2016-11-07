#!/usr/bin/env python
# coding=utf-8

from orm import Model, StringField, IntegerField, BooleanField


class Meal(Model):
    """
    生日餐
    """
    __table__ = 'hitfd_meals'

    id = IntegerField(primary_key=True, updatable=False, ai=True, ddl='int(11)')
    name = StringField(ddl='varchar(50)')  # 套餐名
    picture = StringField(ddl='varchar(200)')  # 图片
    description = StringField(ddl='varchar(1000)')  # 餐品描述
    active = BooleanField()  # 是否有效
    canteenId = IntegerField(ddl='int(7)')  # 餐厅编号
    clock = StringField(ddl='varchar(255)')  # 供餐时间
    sex_condition = IntegerField(ddl='int(1)')  # 性别条件
