#!/usr/bin/env python
#coding=utf-8

prefix = 'models.'

urls = (
        r"/", prefix + "index.index",
        r"/index", prefix +"index.index",


        r"/test", prefix + "index.test",
        
        r"/(.*)",  prefix + "index.err404",
        )
