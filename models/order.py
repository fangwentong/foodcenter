#!/usr/bin/env python2
#coding=utf-8

from config import setting
import web

render = setting.render

class index:
	def GET(self):
		return render.order.index("order", U"欢迎使用订餐系统")
	def POST(self):
		pass
		#

class signup:
	def GET(self):
		return render.order.signup("order", U"注册")
	def POST(self):
		info = web.input()

class signin:
	def GET(self):
		return render.order.signin("order", U"用户登陆")
	def POST(self):
		raise web.seeother("/order/info")

class add_order:
	def GET(self):
		return render.order.addorder("order", U"添加订单")
	def POST(self):
		web.seeother("/order/info")

class get_info:
	def GET(self):
		return render.order.orderinfo("order", "订单信息")
