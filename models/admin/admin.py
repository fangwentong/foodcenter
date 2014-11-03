#!/usr/local/env python2
#coding=utf-8


import web
from config import setting

render = setting.render

class signin:
	def GET(self):
		return render.admin.login("", setting.admin.title)
	def POST(self):
		raise web.seeother


class index:
	def GET(self):
		pass
	def POST(self):
		pass

