#!/usr/bin/env python2
#coding=utf-8

from config import setting
import web

render = setting.render
db     = setting.db

def sessionChecker(func):
    def _sessionChecker(*args, **kwargs):
        # print ("Before {} is called.".format(func.__name__))
        session = web.config._session
        try:
            #尚未登录
            if not session.logged or session.role is not "student":
                raise web.seeother('/order/signin')
            #已经登录且为学生
            elif session.logged and session.role is"student":
                ret = func(*args, **kwargs)
        except Exception as err:
            print err
            return render.errinfo("order", U"出错啦", err)
        # print ("After {} is called".format(func.__name__))
        return ret
    return _sessionChecker

class index:
    def GET(self):
        return render.order.index("order", "生日餐预定", web.config._session)
    def POST(self):
        pass

class signup:
    def GET(self):
        return render.order.signup("order", U"注册", "")

    def POST(self):
        user_info = web.input()

        try:                   #查数据表，判断是否注册
            sql = "SELECT * FROM foodcenter_users WHERE student_id=$sid"
            result = list(db.query(sql, vars={'sid':user_info.sid}))
        except Exception as err:
            print err
            return render.errinfo("feedback", U"出错啦", err)

        if len(result) >= 1: #已注册,自动跳转
            print("Already Registerd!")
            raise web.seeother("/order/info")
        else:      #未注册
            sql = "SELECT * FROM foodcenter_students WHERE student_id=$sid AND student_name=$name"
            result = list(db.query(sql, vars={'sid':user_info.sid, 'name':user_info.name}))

            if len(result) <= 0:          #学生身份验证
                errinfo = "学生身份验证出错，请输入正确的学生信息."
                print errinfo
                return render.order.signup("order", U"注册", errinfo)

            try:      #验证通过， 插入新的表项
                db.insert('foodcenter_users',
                        student_id    = user_info.sid,
                        student_name  = user_info.name,
                        sex           = self.getSexId(user_info.sex),
                        birthday      = user_info.birthday,
                        phone         = user_info.phone,
                        short_message = user_info.message,
                        weixinId      = "",
                        add_time      = web.SQLLiteral("NOW()"),
                        isLock        = 0
                        )
                raise web.seeother("/order/info")
            except Exception as err:
                print err
                return render.errinfo("order", U"出错啦", err)

    def getSexId(self, sex):
        if sex == "boy":
            return 0
        elif sex == "girl":
            return 1
        else:
            print ("Invalid Sex!\n")
            return -1

class signin:
    def GET(self):
        return render.order.signin("order", U"用户登陆", "")
    def POST(self):
        info = web.input()  #sid & name
        print info.sid
        print info.name
        try:
            sql = "SELECT * FROM foodcenter_users WHERE student_id=$sid AND student_name=$name"
            result = list(db.query(sql, vars={'sid' : info.sid, 'name' : info.name}))

            if len(result) <= 0:          #学生身份验证
                errinfo = "您输入的学号和姓名不匹配，请检查后重试."
                print errinfo
                return render.order.signin("order", U"登录", errinfo)
            else:
                web.config._session.name   = result[0].student_name
                web.config._session.sid    = result[0].student_id
                web.config._session.role   = "student"
                web.config._session.logged = True
                raise web.seeother("/order/info")

        except Exception as err:
            print err
            return render.errinfo("order", U"出错啦", err)


class add_order:
    @sessionChecker
    def GET(self):
        return render.order.addorder("order", U"添加订单", "")
    def POST(self):
        #raise web.seeother("/order/info")
        pass

class get_info:
    @sessionChecker
    def GET(self):
        # 获取用户信息
        sql        = "SELECT * FROM foodcenter_users WHERE student_id=$sid AND student_name=$name"
        stu_info   = list(db.query(sql, vars={'sid' : web.config._session.sid, 'name' : web.config._session.name}))
        # 获取订单信息
        sql        = "SELECT * FROM foodcenter_orders WHERE student_id=$sid AND active=1"
        order_info = list(db.query(sql, vars={'sid' : web.config._session.sid}))

        data = web.storage (
                user  = stu_info[0],
                order = order_info
                )
        return render.order.orderinfo("order", U"订单信息", data)
    def POST(self):
        pass

class get_help:
    def GET(self):
        return render.order.orderhelp("order", U"订餐帮助")
    def POST(self):
        pass
