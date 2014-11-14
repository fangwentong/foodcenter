#!/usr/local/env python2
#coding=utf-8


import web
from config import setting

render = setting.render
db = setting.db

class Index:
    def GET(self):
        return render.admin.index("index", "饮食中心后台管理系统", "")
        #pass
    def POST(self):
        pass

class LogIn:
    def GET(self):
        return render.admin.login("", setting.admin.title)
    def POST(self):
        data = web.input()
        #print data

        try:
            result = db.query("SELECT * FROM foodcenter_admins WHERE username=$username",
                    vars = {'username' : data.username})
            print result

        except Exception as err:
            print err

        if hasattr(data, "remeber"):
            print "Remeber Login State"

        #raise web.seeother
        pass
class LogOut:
    def GET(self):
        pass
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
        return render.admin.meals("orderings", "套餐管理", "")
    def POST(self):
        pass

class AddMeal:
    def GET(self):
        return render.admin.meals("orderings", "添加套餐", "")
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

