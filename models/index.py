#!/usr/bin/env python
#coding=utf-8

from config import setting
import web

render = setting.render

class index:
    def GET(self):
        return render.index('index')

class err404:
	def GET(self):
		return render.err404('err404')
