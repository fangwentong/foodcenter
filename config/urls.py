#!/usr/bin/env python
#coding=utf-8

prefix = 'models.'

urls = (
        r"/",                          prefix + "home.index",
        r"/index",                     prefix + "home.index",
        r"/about",                     prefix + "home.about",
        r"/contact",                   prefix + "home.contact",
        r"/help",                      prefix + "home.help",
        r"/canteen",                   prefix + "home.canteen",
        r"/feedback",                  prefix + "home.feedback",

        r"/order",                     prefix + "order.index",



        r"/test",                      prefix + "home.test",
        r"/(.*)",                      prefix + "home.err404",
        )
