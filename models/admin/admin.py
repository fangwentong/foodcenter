#!/usr/bin/env python2
#coding=utf-8

from config import setting
import web

render = setting.render

class signin:
	def GET(self):
		return render.admin.login("", setting.admin.title)
	def POST(self):
		pass