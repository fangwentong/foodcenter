#!/usr/bin/env python
#coding=utf-8

import web
import os
import time
from secret import secrets

render = web.template.render('templates/', cache=False)

web.config.debug = True

site = web.storage (
        title  = U"哈工大饮食中心",
        brand  = U"哈工大饮食中心",
        root   = "http://foodcenter.sinaapp.com",

        date   = web.storage (
            year  = time.strftime('%Y',time.localtime(time.time())),
            month = time.strftime('%m',time.localtime(time.time())),
            day   = time.strftime('%d',time.localtime(time.time())),
            ),

        owner = web.storage (
            name = U"哈尔滨工业大学 饮食中心",
            site = "#",
            ),

        author = web.storage (
            name     = "fangwentong",
            email    = "fangwentong2012@gmail.com",
            home     = "http://www.fangwentong.com",
            org      = "Pureweber",
            org_site = "http://www.pureweber.com",
            ),

        )

login = web.storage (
        title = U"饮食中心后台管理系统--登陆",
        )

if 'SERVER_SOFTWARE' in os.environ:
    asset_path = "/static"
    # image_url = "http://hitfoodcenter.qiniudn.com/image"
    image_url = "/static/image"
else:
    asset_path = "/static"
    image_url = "/static/image"

web.template.Template.globals['site'] = site
web.template.Template.globals['render'] = render
web.template.Template.globals['asset_path'] = asset_path
web.template.Template.globals['image_url'] = image_url
