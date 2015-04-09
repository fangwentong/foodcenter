#!/usr/bin/env python
#coding=utf-8

from orm import Model, StringField, IntegerField

class Student(Model):
    """
    学生
    """
    __table__ = 'foodcenter_students'

    id          = IntegerField(primary_key=True, updatable=False, ai=True, ddl='int(12)')
    studentId   = StringField(ddl='varchar(64)', updatable=False)    # 学号
    StudentName = StringField(ddl="varchar(255)", updatable=False)   # 姓名
    sex         = StringField(ddl="varchar(10)");                    # 性别
    identity    = StringField(ddl="varchar(20)", updatable=False);   # 身份证号码
    add_year    = StringField(ddl="year(4)")                         # 入学年份


