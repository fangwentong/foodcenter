#!/usr/bin/env python
#coding=utf-8

from config import setting

render = setting.render

class index:
    def GET(self):
        return render.index()

class err404:
	def GET(self):
		return render.err404()
