#!/usr/local/env python2
#coding=utf-8


import web
from config import setting

render = setting.render
db = setting.db

class login:
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


class index:
    def GET(self):
        return render.admin.index("widgets", "饮食中心后台管理系统", "")
        #pass
    def POST(self):
        pass

