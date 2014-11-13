#!/usr/local/env python2
#coding=utf-8


import web
from config import setting

render = setting.render
db = setting.db

class Index:
    def GET(self):
        return render.admin.index("widgets", "饮食中心后台管理系统", "")
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
        pass
    def POST(self):
        pass

class ChgPasswd:
    def GET(self):
        pass
    def POST(self):
        pass

class DashBoard:
    def GET(self):
        pass
    def POST(self):
        pass

class Orderings:
    def GET(self):
        pass
    def POST(self):
        pass

class GetMeals:
    def GET(self):
        pass
    def POST(self):
        pass

class AddMeal:
    def GET(self):
        pass
    def POST(self):
        pass

class Feedback:
    def GET(self):
        pass
    def POST(self):
        pass

class Users:
    def GET(self):
        pass
    def POST(self):
        pass

class AddUser:
    def GET(self):
        pass
    def POST(self):
        pass

