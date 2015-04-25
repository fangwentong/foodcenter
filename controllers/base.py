#!/usr/bin/env python
#coding=utf-8

import web
import os, sys
app_root = os.path.join(os.path.dirname(__file__), os.path.pardir)
sys.path.insert(0, app_root)

from config import render, site
from models import User

class BasePage:
    """网站页面基类"""
    def __init__(self, page_name, page_title):
        self.page = web.storage(
                name = page_name,
                title = page_title,
                errinfo = ""
                )
    def POST(self):
        pass

class Article:
    """新闻页面基类"""
    def __init__(self, page_name="", page_title="", page_url="", page_id=100):
        self.page = web.storage(
                name    = page_name,
                title   = page_title,
                url     = site.root + page_url,
                page_id = page_id
                )
    def POST(self):
        pass

class StuAuth:
    """
    用于身份验证的工具类
    """
    def __init__(self, page_name="", page_title=""):
        self.session = web.config._session
        self.page    = web.storage(
                name  = page_name,
                title = page_title,
                errinfo = ""
                )
        # print("An Object was created, which id {}".format(id(self)))

    @staticmethod
    def decoder(func):
        """
        URL解编码装饰器, 提供URL参数登陆支持
        """
        def _decoder(*args, **kwargs):
            print ("Before {} is called.".format(func.__name__))
            data = web.input(wid='')
            if StuAuth.isValid(data.wid): # 通过URL编码方式登陆
                result = User.getBy(weixinId = data.wid)

                if result:
                    web.config._session.name   = result.studentName
                    web.config._session.sid    = result.studentId
                    web.config._session.phone  = result.phone
                    web.config._session.role   = "student"
                    web.config._session.logged = True
                else:
                    if web.config._session.logged and web.config._session.role == "student":
                        person = User.getBy(studentId = web.config._session.sid)
                        if not person.weixinId:
                            person.weixinId = data.wid
                            person.update()
                    web.config._session.weixinId = data.wid
                return web.seeother("")
            else:
                ret = func(*args, **kwargs)
            print ("After {} is called.".format(func.__name__))
            return ret
        return _decoder

    @staticmethod
    def sessionChecker(func):
        """
        session 检查装饰器
        """
        def _sessionChecker(*args, **kwargs):
            print ("Before {} is called.".format(func.__name__))
            try:
                #尚未登录
                if not web.config._session.logged or web.config._session.role != "student":
                    return web.seeother("/order")
                #已经登录且为学生
                else:
                    ret = func(*args, **kwargs)
            except Exception as err:
                return StuAuth.error(err)
            print ("After {} is called.".format(func.__name__))
            return ret
        return _sessionChecker

    @staticmethod
    def error(msg, page_name="order", page_title="出错啦"):
        """
        返回错误页面
        """
        print msg
        return render.errinfo(page = web.storage(
                name    = page_name,
                title   = page_title,
                errinfo = msg
            ))

    @staticmethod
    def success(msg):
        """
        返回成功页面
        """
        print msg

    @staticmethod
    def isValid(weixinId):
        """
        简单地判断OpenID是否有效
        """
        if len(weixinId) <= 15:
            return False
        else:
            return True
