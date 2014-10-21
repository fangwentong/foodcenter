#!/usr/bin/env python
#coding=utf-8

from config import setting
import web

render = setting.render

class index:
	def GET(self):
		return render.order.index("order", U"欢迎使用订餐系统")

class signup:
	def GET(self):
		return render
	def POST(self):
		info = web.data()

class add_order:
	def GET(self):
		return render

class get_info:
	def GET(self):
		return render
