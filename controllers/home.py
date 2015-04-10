#!/usr/bin/env python2
#coding=utf-8

from config import setting
from base import BasePage
from models import FeedBack, Article
import web, json

render = setting.render
db = setting.db

def notfound():
    return web.notfound(render.err404(page = web.storage(name="err404", title=U"链接不存在")))

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
        return render.index(page = self.page)


class test(BasePage):
    """
    测试页面
    """
    def __init___(self):
        BasePage.__init__(self, "test", U"测试页面")
    def GET(self):
        return render.test(page = self.page)

class about(BasePage):
    """
    关于我们
    """
    def __init__(self):
        BasePage.__init__(self, "about", U"关于我们 - 哈工大饮食中心")
    def GET(self):
        return render.pages.aboutus(page = self.page)

class contact(BasePage):
    """
    联系我们
    """
    def __init__(self):
        BasePage.__init__(self, "contactus", U"联系我们 - 哈工大饮食中心")
    def GET(self):
        return render.pages.contactus(page = self.page)

class help(BasePage):
    """
    常见问题
    """
    def __init__(self):
        BasePage.__init__(self, "generalhelp", U"常见问题 - 哈工大饮食中心")
    def GET(self):
        return render.pages.generalhelp(page = self.page)

class canteen(BasePage):
    """
    餐厅特色
    """
    def __init__(self):
        BasePage.__init__(self, "canteen", U"餐厅特色 - 哈工大饮食中心")
    def GET(self):
        return render.pages.canteen(page = self.page)

class feedback(BasePage):
    """
    意见反馈
    """
    def __init__(self):
        BasePage.__init__(self, "feedback", U"意见反馈 - 哈工大饮食中心")
    def GET(self):
        return render.pages.feedback(page = self.page)
    def POST(self):
        data = web.input(req = '', username = '', feedback = '')
        if data.req == 'submit':
            if data.username == '':
                return json.dumps({'errinfo' : '请输入您的姓名'})
            if data.feedback == '':
                return json.dumps({'errinfo' : '请输入您的反馈'})
            try:
                FeedBack({
                    "name": data.username,
                    "email": data.email,
                    "phone": data.phone,
                    "content": data.feedback,
                }).insert()
                return json.dumps({'successinfo' : '已收到您的反馈，我们会尽快解决您的问题 ^_^'})
            except Exception:
                pass
                # return json.dumps({'errinfo' : '出现错误: ' + str(err)})
        else:
            return web.Forbidden()


class GetArticle:
    def GET(self):
        page_id = web.input(id="").id

        if page_id == "":
            # 获取文章列表
            return web.notfound(render.err404(page = web.storage(name="err404", title=U"链接不存在")))
        else:
            try:
                article = Article.getBy(id = page_id, isDraft = False)

                if article == None:
                    return web.notfound(render.err404(page = web.storage(name="err404", title=U"链接不存在")))
                return render.pages.article(page = web.storage(
                    title = article.title,
                    name  = "title"
                    ), article = article)

            except Exception as err:
                return render.errinfo(page = web.storage(
                    name = "article",
                    title = "出错啦",
                    errinfo = err
                    ))
    def POST(self):
        pass
