#!/usr/bin/env python2
#coding=utf-8

from config import setting
import web

render = setting.render
db     = setting.db

class index:
    def GET(self):
        return render.order.index("order", U"欢迎使用订餐系统")
    def POST(self):
        pass
        #

class signup:
    def GET(self):
        return render.order.signup("order", U"注册")
    def POST(self):
        user_info = web.input()
        #print data

        try:
            db.insert('foodcenter_users',
                    sid      = user_info.sid,
                    name     = user_info.name,
                    birthday = user_info.birthday,
                    phone    = user_info.phone,
                    message  = user_info.message,
                    addTime = web.SQLLiteral("NOW()")
                    )
            raise web.seeother("/order/info")
        except Exception as err:
            print err
            return render.errinfo("feedback", U"出错啦", err)

class signin:
    def GET(self):
        return render.order.signin("order", U"用户登陆")
    def POST(self):
        #raise web.seeother("/order/info")
        pass


class add_order:
    def GET(self):
        return render.order.addorder("order", U"添加订单")
    def POST(self):
        #raise web.seeother("/order/info")
        pass

class get_info:
    def GET(self):
        return render.order.orderinfo("order", "订单信息")
