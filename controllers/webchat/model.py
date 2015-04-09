#!/usr/bin/env python2
#coding=utf-8

all = ['robot']

import os, sys

current_path = os.path.dirname(__file__)
app_root = os.path.join(current_path, os.path.pardir, os.path.pardir)
sys.path.insert(0, app_root)             # 网站根目录加入搜索路径

from config import db

############## Models ##################
def get_package_name(package_id):
    try:
        sql = "SELECT * FROM foodcenter_meals WHERE id=$id"
        result = list(db.query(sql, vars={'id' : str(package_id)}))
        if len(result) > 0:
            return result[0].name
        else:
            return "没有找到匹配的套餐"
    except Exception as err:
        return "出现错误: " + str(err)

def get_canteen_name(canteen_id):
    try:
        sql = "SELECT * FROM foodcenter_canteen WHERE cid=$cid"
        result = list(db.query(sql, vars={'cid' : canteen_id}))
        if len(result) > 0:
            return result[0].name
        else:
            return "没有找到匹配的餐厅"
    except Exception as err:
        return "出现错误: " + str(err)

def authchecker(func):
    """
    管理员权限验证
    """
    def _authchecker(message):
        try:
            sql = "SELECT * FROM foodcenter_cmd_admins WHERE WeixinId=$wx_id"
            result = list(db.query(sql, vars={'wx_id' : message.source}))
            if len(result) <= 0:
                pass
            else:
                return func(message)

        except Exception as err:
            return "出现错误: " + str(err)
    return _authchecker
