#!/usr/bin/env python
#coding=utf-8

from orm import Model, StringField, IntegerField, BooleanField

class Meal(Model):
    __table__ = 'foodcenter_meals'

    id       = IntegerField(primary_key=True, nullable=False, ddl='int(11)')
    name  = StringField(ddl='varchar(50)')
    picture = StringField(ddl="varchar(200)")
    description = StringField(ddl='varchar(1000)')
    active = BooleanField(ddl="boolean")
    canteen = IntegerField(ddl="int(7)")
    clock = StringField(ddl="varchar(255)")
    location = IntegerField(ddl="int(2)")
    sex_condition = IntegerField(ddl="int(1)")


