#!/usr/bin/env python
#coding=utf-8

from orm import Model, StringField, IntegerField

class Canteen(Model):
    """
    餐厅
    """
    __table__ = 'foodcenter_canteens'

    id         = IntegerField(primary_key=True, nullable=False, ddl='int(11)')
    name       = StringField(ddl='varchar(50)')    # 餐厅名
    picture    = StringField(ddl='varchar(100)')   # 图片
    desription = StringField(ddl='varchar(2000)')  # 简介
    location   = IntegerField(ddl='int(5)')        # 校区
    address    = StringField(ddl='varchar(255)')   # 详细地址描述

