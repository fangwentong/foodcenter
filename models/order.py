#!/usr/bin/env python
# coding = utf-8

import web

class index:
	def GET(self):
		return render.order.index("order", U"欢迎使用订餐系统")