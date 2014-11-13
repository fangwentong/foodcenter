#!/usr/bin/env python2
#coding=utf-8

prefix = "models.admin."

urls = (
        r"",                    prefix + "admin.index",
        r"/",                   prefix + "admin.index",

        r"/login",              prefix + "admin.login",
        r"/logout",             prefix + "admin.logout",
        r"/profile",            prefix + "admin.GetProfile",
        r"/settings",           prefix + "admin.",

        
        )
