#!/usr/bin/env python
#coding=utf-8

from orm import Model, StringField, IntegerField

class CmdAdmin(Model):
    __table__ = 'foodcenter_cmd_admins'

    id       = IntegerField(primary_key=True, nullable=False, ddl='int(11)')
    username = StringField(ddl='varchar(255)')
    password = StringField(ddl='varchar(255)')
    weixinId = StringField(ddl="varchar(255)")
    role     = IntegerField(ddl="int(11)")

