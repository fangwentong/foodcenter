#!/usr/bin/env python2
#coding=utf-8

from config import setting
import web

render = setting.render
db = setting.db

def notfound():
    return web.notfound(render.err404("err404", U"链接不存在"))

class index:
    def GET(self):
        return render.index("home", U"哈工大饮食中心")
    def POST(self):
        pass

class redirect:
    def GET(self, path):
        web.seeother("/"+path)
    def POST(self):
        pass

class test:
    def GET(self):
        return render.test("test", U"测试页面")
    def POST(self):
        pass

class about:
    def GET(self):
        return render.pages.aboutus("about", U"关于我们")
    def POST(self):
        pass

class contact:
    def GET(self):
        return render.pages.contactus("contactus", U"联系我们")
    def POST(self):
        pass

class help:
    def GET(self):
        return render.pages.generalhelp("generalhelp", U"常见问题")
    def POST(self):
        pass

class canteen:
    def GET(self):
        return render.pages.canteen("canteen", U"餐厅特色")
    def POST(self):
        pass

class feedback:
    def GET(self):
        return render.pages.feedback("feedback", U"意见反馈")
    def POST(self):
        data = web.input()
        #print data

        try:
            db.insert('foodcenter_feedbacks',
                    name    = data.username,
                    email   = data.email,
                    phone   = data.phone,
                    content = data.feedback,
                    solved  = 0,
                    addTime = web.SQLLiteral("NOW()")
                    )
            return render.pages.feedback_success("feedback", U"反馈成功")
        except Exception as err:
            print err
            return render.errinfo("feedback", U"出错啦", err)
