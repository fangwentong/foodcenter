#!/usr/bin/env python2
#coding=utf-8

from controllers import admin

prefix = 'controllers.'

urls = (
        r"",                           prefix + "home.index",
        r"/",                          prefix + "home.index",
        r"/(.*)/",                     prefix + "home.redirect",
        r"/index",                     prefix + "home.index",
        r"/about",                     prefix + "home.about",
        r"/contact",                   prefix + "home.contact",
        r"/help",                      prefix + "home.help",
        r"/canteen",                   prefix + "home.canteen",
        r"/feedback",                  prefix + "home.feedback",
        r"/article",                   prefix + "home.GetArticle",

        r"/order",                     prefix + "order.index",
        r"/order/signup",              prefix + "order.signup",
        r"/order/signin",              prefix + "order.signin",
        r"/order/logout",              prefix + "order.logout",
        r"/order/add",                 prefix + "order.add_order",
        r"/order/info",                prefix + "order.get_info",
        r"/order/help",                prefix + "order.get_help",

        r"/admin",                     admin.management_app,

        r"/we/WeixinInterface",        prefix + "webchat.WeixinHandler",

        r"/test",                      prefix + "home.test"
        )
