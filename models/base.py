#!/usr/bin/env python
#coding=utf-8

import web
from config import setting

db     = setting.db
render = setting.render

class BasePage:
    """网站页面基类"""
    def __init__(self, page_name, page_title):
        """
        __init__
        """
        self.page = web.storage(
                name = page_name,
                title = page_title,
                errinfo = ""
                )

class Article:
    """新闻页面基类"""
    def __init__(self, page_name="", page_title="", page_url="", page_id=100):
        """
        __init__
        """
        self.page = web.storage(
                name    = page_name,
                title   = page_title,
                url     = setting.site.root + page_url,
                page_id = page_id
                )


class StuAuth:
    """
    用于身份验证的工具类
    """
    def __init__(self, page_name="", page_title=""):
        """
        __init__
        """
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

            data = web.input(wid='-')
            if StuAuth.isValid(data.wid):
                try:         # 通过URL编码方式登陆
                    sql = "SELECT * FROM foodcenter_users WHERE weixinId = $wx_id" #验证微信账户信息
                    result = list(db.query(sql, vars={'wx_id':data.wid}))

                    if len(result) > 0:
                        web.config._session.name   = result[0].student_name
                        web.config._session.sid    = result[0].student_id
                        web.config._session.role   = "student"
                        web.config._session.logged = True
                    else:
                        if hasattr(web.config._session, "logged") and web.config._session.logged == True \
                            and web.config._session.role == "student":
                            sql = "SELECT * FROM foodcenter_users WHERE student_name=$name"
                            print web.config._session.name
                            result = list(db.query(sql, vars={'name' : web.config._session.name}))
                            if len(result) > 0 and result[0].weixinId == "":
                                db.update('foodcenter_users', web.db.sqlwhere({'student_name' : web.config._session.name}),
                                        weixinId = data.wid)
                        else:
                            web.config._session.wid = data.wid
                    return web.seeother("")
                except Exception as err:
                    return StuAuth.error(err)
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
                    return web.seeother("/order/signup")
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
        return render.errinfo(web.storage(
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
        if len(weixinId) <= 20:
            return False
        else:
            return True
