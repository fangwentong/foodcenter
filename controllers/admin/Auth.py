#!/usr/bin/env python
#coding=utf-8

import web
from config import render

class AdminAuth:
    """
    用于管理员身份验证的工具类
    """
    def __init__(self, page_name="", page_title=""):
        """
        __init__
        """
        self.session  = web.config._session
        self.page = web.storage(
                name         = page_name,
                title        = page_title,
                errinfo      = "",
                successsinfo = ""
                )
        # print("An Object was created, which id {}".format(id(self)))

    def POST(self):
        pass

    @staticmethod
    def sessionChecker(func):
        """
        session 检查装饰器
        """
        def _sessionChecker(*args, **kwargs):
            # print ("Before {} is called.".format(func.__name__))
            try:
                # 管理员尚未登录
                if not web.config._session.logged or web.config._session.role != "admin":
                    return web.seeother("/login")
                # 已经登录且为管理员
                else:
                    ret = func(*args, **kwargs)
            except Exception as err:
                return AdminAuth.error(err)
            # print ("After {} is called.".format(func.__name__))
            return ret
        return _sessionChecker

    @staticmethod
    def error(msg, pagename="", pagetitle="出错啦"):
        """
        返回错误页面
        """
        print msg
        return render.admin.error(
                page = web.storage(
                    name    = pagename,
                    title   = pagetitle,
                    errinfo = msg
                    ),
                session = web.config._session)

    @staticmethod
    def success(msg):
        """
        返回成功页面
        """
        print msg
