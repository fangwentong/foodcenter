#!/usr/bin/env python
#coding=utf-8


from orm import Model, StringField, IntegerField

class Admin(Model):
    __table__ = 'foodcenter_admins'

    id       = IntegerField(primary_key=True, nullable=False, ddl='int(11)')
    username = StringField(ddl='varchar(255)')
    password = StringField(ddl='varchar(255)')
    role     = IntegerField(ddl="int(11)")
    nickname = StringField(ddl="varchar(64)")
    email    = StringField(ddl="varchar(128)")

