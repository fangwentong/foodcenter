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
		return render.order.add_order("order", U"添加订单")
	def POST(self):
		web.seeother("/order/info")

class get_info:
	def GET(self):
		return render.order.orderinfo("order", "订单信息")
