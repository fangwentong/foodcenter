#!/usr/local/env python2
#coding=utf-8

import web
import hashlib
from config import setting

render = setting.render
db = setting.db

class Index:
    def GET(self):
        try:
            #尚未登录
            if web.config._session.logged == False:
                return web.seeother('/login')
            #已经登录且为管理员
            elif web.config._session.logged == True and web.config._session.role == "admin":
                return web.seeother('/dashboard')
        except Exception as err:
            print err
            return render.errinfo("order", U"出错啦", err)
    def POST(self):
        pass

class LogIn:
    def GET(self):
        return render.admin.login("admin", "管理员登录", "")
    def POST(self):
        data = web.input(remeber="")   #username password remeber
        #print data

        try:
            sql = "SELECT * FROM foodcenter_admins WHERE username=$username AND password=$password"
            result = list(db.query(sql, vars={'username' : data.username, 'password' : hashlib.new("md5", data.password).hexdigest()}))

            if len(result) <= 0:    #身份验证失败
                errinfo = "您输入的学号和姓名不匹配，请检查后重试."
                print errinfo
                return render.admin.login("admin", U"管理员登录", errinfo)
            else:
                web.config._session.name   = result[0].username
                web.config._session.role   = "admin"
                web.config._session.logged = True
                if data.remeber:      #记住密码
                    web.config.session_parameters['ignore_expiry'] = True
                raise web.seeother("/dashboard")

        except Exception as err:
            print err
            return render.errinfo("order", U"出错啦", err)

        if hasattr(data, "remeber"):
            print "Remeber Login State"


class LogOut:
    def GET(self):
        web.config._session.kill()
        raise web.seeother('/')
    def POST(self):
        pass

class GetProfile:
    def GET(self):
        return render.admin.profiles("profile", "个人资料", "")
    def POST(self):
        pass

class ChgPasswd:
    def GET(self):
        return render.admin.settings("setting", "设置", "")
    def POST(self):
        pass

class DashBoard:
    def GET(self):
        return render.admin.dashboard("dashboard", "仪表盘", "")
    def POST(self):
        pass

class Orderings:
    def GET(self):
        return render.admin.orderings("orderings", "订单管理", "")
    def POST(self):
        pass

class GetMeals:
    def GET(self):
        return render.admin.meals("meals", "套餐管理", "")
    def POST(self):
        pass

class AddMeal:
    def GET(self):
        return render.admin.meals("meals", "添加套餐", "")
    def POST(self):
        pass

class Feedback:
    def GET(self):
        return render.admin.feedback("feedback", "反馈处理", "")
    def POST(self):
        pass

class Users:
    def GET(self):
        return render.admin.users("users", "用户管理", "")
    def POST(self):
        pass

class AddUser:
    def GET(self):
        return render.admin.users("users", "添加用户", "")
    def POST(self):
        pass

