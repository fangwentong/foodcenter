#!/usr/bin/env python
#coding=utf-8

from config import setting
import web

render = setting.render

class index:
    def GET(self):
        return render.index("home", U"哈尔滨工业大学饮食中心")

class err404:
	def GET(self, url):
		return render.err404("err404", U"链接不存在")

class test:
	def GET(self):
		return render.test("test", U"测试页面")

class about:
	def GET(self):
		return render.pages.aboutus("about", U"关于我们")

class contact:
	def GET(self):
		return render.pages.contactus("contactus", U"联系我们")

class help:
	def GET(self):
		return render.pages.generalhelp("generalhelp", U"常见问题")
class canteen:
	def GET(self):
		return render.pages.canteen("canteen", U"餐厅特色")