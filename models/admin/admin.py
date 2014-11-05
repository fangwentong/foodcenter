#!/usr/local/env python2
#coding=utf-8


import web
from config import setting

render = setting.render
db = setting.db

class signin:
    def GET(self):
        return render.admin.login("", setting.admin.title)
    def POST(self):
        data = web.input()
        #raise web.seeother
        pass


class index:
    def GET(self):
        return render.admin.login("", setting.admin.title)
        #pass
    def POST(self):
        pass

