#!/usr/bin/env python2
#coding=utf-8

prefix = 'models.'

urls = (
        r"/",                          prefix + "home.index",
        r"/(.*)/",                     prefix + "home.redirect",
        r"/index",                     prefix + "home.index",
        r"/about",                     prefix + "home.about",
        r"/contact",                   prefix + "home.contact",
        r"/help",                      prefix + "home.help",
        r"/canteen",                   prefix + "home.canteen",
        r"/feedback",                  prefix + "home.feedback",

        r"/order",                     prefix + "order.index",
        r"/order/signup",              prefix + "order.signup",
        r"/order/signin",              prefix + "order.signin",
        r"/order/add",                 prefix + "order.add_order",
        r"/order/info",                prefix + "order.get_info",

        r"/admin/signin",              prefix + "admin.admin.signin",
        r"/admin",                     prefix + "admin.admin.index",

        r"/we/webchat/port",           prefix + "webchat.verify.WeixinInterface",



        r"/test",                      prefix + "home.test",
        r"/(.*)",                      prefix + "home.err404",
        )
