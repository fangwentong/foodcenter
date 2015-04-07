#!/usr/bin/env python
#coding=utf-8

from orm import Model, StringField

class Student(Model):
    __table__ = 'foodcenter_students'

    id       = StringField(primary_key=True, nullable=False, ddl='varchar(64)') # 学号
    name     = StringField(ddl="varchar(255)") #姓名
    sex      = StringField(ddl="varchar(10)"); #性别
    identity = StringField(ddl="varchar(20)"); #身份证号码
    add_year = StringField(ddl="year(4)") #入学年份


