#!/usr/bin/env python
#coding=utf-8


from orm import Model, StringField, IntegerField

class Admin(Model):
    """
    后台管理系统管理员账户
    """
    __table__ = 'foodcenter_admins'

    id       = IntegerField(primary_key=True, ddl='int(11)', updatable=False)
    username = StringField(ddl='varchar(255)')                       # 用户名
    password = StringField(ddl='varchar(255)')                       # 密码
    role     = IntegerField(ddl="int(11)", default=3)                # 角色
    nickname = StringField(ddl="varchar(64)", default="管理员")      # 昵称
    email    = StringField(ddl="varchar(128)")                       # 邮箱

