#!/usr/bin/env python2
#coding=utf-8

import hashlib
import web

TOKEN = "fangwentong"

# 微信接口认证类 WeixinInterface
class WeixinInterface:
    def GET(self):
        data = web.input()  #获取输入参数
        # print data
        try:
            signature = data.signature
            timestamp = data.timestamp
            nonce  = data.nonce
            echostr = data.echostr
            # print "signature : " + signature
            # print "timestamp : " + timestamp
            # print "nonce : " + nonce
            # print "echostr : " + echostr
            args = [TOKEN, timestamp, nonce]
            args.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, args)
            hashcode = sha1.hexdigest()
            if hashcode == signature:
                return echostr
        except Exception as err:
            return err

    def POST(self):
        pass
