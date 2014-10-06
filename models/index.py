#!/usr/bin/env python
#coding=utf-8

from config import setting
import web

render = setting.render

class index:
    def GET(self):
        return render.index("index", U"哈尔滨工业大学饮食中心")

class err404:
	def GET(self, url):
		return render.err404("err404", U"链接不存在")

class test:
	def GET(self):
		return render.test("test", U"测试页面")
