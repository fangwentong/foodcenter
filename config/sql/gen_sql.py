#!/usr/bin/env python
#coding=utf-8

import os, sys

app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
sys.path.insert(0, app_root)

from models import Admin, Article, Canteen, CmdAdmin
from models import Meal, Order, Student, User


SQLS = ["""\
create table foodcenter_sessions (
    `session_id` char(128) unique not null,
    `atime` timestamp not null default current_timestamp,
    `data` text
);"""]

SQLS.append(Admin().__sql__())
SQLS.append(Article().__sql__())
SQLS.append(Canteen().__sql__())
SQLS.append(CmdAdmin().__sql__())
SQLS.append(Meal().__sql__())
SQLS.append(Order().__sql__())
SQLS.append(Student().__sql__())
SQLS.append(User().__sql__())

sql_file_name = os.path.join(os.path.dirname(__file__), 'foodcenter.sql')
fp = open(sql_file_name, 'w')
fp.write("\n".join(SQLS))

print("SQL Sentences have been saved to {}".format(sql_file_name))
