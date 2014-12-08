#!/usr/bin/env python2
#coding=utf-8

from config import setting
from base import BasePage
import web

render = setting.render
db = setting.db

def notfound():
    return web.notfound(render.err404(web.storage(name="err404", title=U"链接不存在")))


class redirect:
    def GET(self, path):
        web.seeother("/"+path)
    def POST(self):
        pass


class index(BasePage):
    """
    首页导航
    """
    def __init__(self):
        BasePage.__init__(self, "home", U"哈工大饮食中心")
    def GET(self):
        return render.index(self.page)
    def POST(self):
        pass


class test(BasePage):
    """
    测试页面
    """
    def __init___(self):
        BasePage.__init__(self, "test", U"测试页面")
    def GET(self):
        return render.test(self.page)
    def POST(self):
        pass

class about(BasePage):
    """
    关于我们
    """
    def __init__(self):
        BasePage.__init__(self, "about", U"关于我们 - 哈工大饮食中心")
    def GET(self):
        return render.pages.aboutus(self.page)
    def POST(self):
        pass

class contact(BasePage):
    """
    联系我们
    """
    def __init__(self):
        BasePage.__init__(self, "contactus", U"联系我们 - 哈工大饮食中心")
    def GET(self):
        return render.pages.contactus(self.page)
    def POST(self):
        pass

class help(BasePage):
    """
    常见问题
    """
    def __init__(self):
        BasePage.__init__(self, "generalhelp", U"常见问题 - 哈工大饮食中心")
    def GET(self):
        return render.pages.generalhelp(self.page)
    def POST(self):
        pass

class canteen(BasePage):
    """
    餐厅特色
    """
    def __init__(self):
        BasePage.__init__(self, "canteen", U"餐厅特色 - 哈工大饮食中心")
    def GET(self):
        return render.pages.canteen(self.page)
    def POST(self):
        pass

class feedback(BasePage):
    """
    意见反馈
    """
    def __init__(self):
        BasePage.__init__(self, "feedback", U"意见反馈 - 哈工大饮食中心")
    def GET(self):
        return render.pages.feedback(self.page)
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
            self.page.title = "反馈成功"
            return render.pages.feedback_success(self.page)
        except Exception as err:
            print err
            self.page.title   = "出错啦"
            self.page.errinfo = err
            return render.errinfo(self.page)
