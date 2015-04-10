#!/usr/bin/env python2
#coding=utf-8

all = ['robot']

import os, sys

current_path = os.path.dirname(__file__)
app_root = os.path.join(current_path, os.path.pardir, os.path.pardir)
sys.path.insert(0, app_root)             # 网站根目录加入搜索路径

import template
from models import CmdAdmin

############## Models ##################
def print_orders(order):
    return template.orderinfo.format(order.name, order.canteen,
                order.studentName, order.studentId, order.birthday)

def authchecker(func):
    """
    管理员权限验证
    """
    def _authchecker(message):
        try:
            result = CmdAdmin.getBy(weixinId = message.source)
            if result == None:
                pass
            else:
                return func(message)
        except Exception as err:
            return "出现错误: " + str(err)
    return _authchecker
