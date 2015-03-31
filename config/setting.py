#!/usr/bin/env python
#coding=utf-8

import web
import os
import time

try:
    import secret
except ImportError:
    import secret_sample as secret
db = secret.db
weconf =secret.webchat

from utils import JinjaRender
render = JinjaRender('templates', encoding='utf-8')
# render = web.template.render('templates', cache=False)

web.config.debug = True

# 站点信息
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
            home     = "http://wentong.me",
            org      = "Pureweber",
            org_site = "http://www.pureweber.com",
            ),
        )

# 后台管理系统配置
admin = web.storage (
        title = U"Food",
        tagline = U"Center",
        )

if 'SERVER_SOFTWARE' in os.environ:
    asset_path = site.root + "/static"
    # image_url = "http://hitfoodcenter.qiniudn.com/image"
    image_url = site.root + "/static/image"
else:
    asset_path = "/static"
    image_url = "/static/image"

# Jinja2 globals
render._lookup.globals.update(
    site = site,
    admin = admin,
    asset_path = asset_path,
    image_url = image_url
)