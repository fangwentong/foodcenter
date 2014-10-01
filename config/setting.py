#!/usr/bin/env python
#coding=utf-8

import web

render = web.template.render('templates/', cache=False)

web.config.debug = True
