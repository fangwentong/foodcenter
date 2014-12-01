#!/usr/bin/env python2
#coding=utf-8

from config import setting
from StuAuth import StuAuth
import web

render = setting.render
db     = setting.db


class index(StuAuth):
    """
    订餐导航
    """
    def __init__(self):
        StuAuth.__init__(self)

    @StuAuth.decoder
    def GET(self):
        return render.order.index("order", "生日餐预定", self.session)

    def POST(self):
        pass


class signup(StuAuth):
    """
    用户注册
    """
    def __init__(self):
        StuAuth.__init__(self)

    @StuAuth.decoder
    def GET(self):
        return render.order.signup("order", U"注册", "")

    def POST(self):
        user_info = web.input()

        try:                   #查数据表，判断是否注册
            sql = "SELECT * FROM foodcenter_users WHERE student_id=$sid"
            result = list(db.query(sql, vars={'sid':user_info.sid}))
        except Exception as err:
            return self.error(err)

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
                return self.error(err)

    def getSexId(self, sex):
        if sex == "boy":
            return 0
        elif sex == "girl":
            return 1
        else:
            print ("Invalid Sex!\n")
            return -1


class signin(StuAuth):
    """
    登陆类
    """
    def __init__(self):
        StuAuth.__init__(self)

    @StuAuth.decoder
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
            return self.error(err)

class add_order(StuAuth):
    """
    添加订单
    """
    def __init__(self):
        StuAuth.__init__(self)

    @StuAuth.decoder
    @StuAuth.sessionChecker
    def GET(self):
        return render.order.addorder("order", U"添加订单", "")

    @StuAuth.sessionChecker
    def POST(self):
        #raise web.seeother("/order/info")
        pass


class get_info(StuAuth):
    """
    获取用户信息
    """
    def __init__(self):
        StuAuth.__init__(self)

    @StuAuth.decoder
    @StuAuth.sessionChecker
    def GET(self):
        # 获取用户信息
        try:
            sql        = "SELECT * FROM foodcenter_users WHERE student_id=$sid AND student_name=$name"
            stu_info   = list(db.query(sql, vars={'sid' : self.session.sid, 'name' : self.session.name}))
            # 获取订单信息
            sql        = "SELECT * FROM foodcenter_orders WHERE student_id=$sid AND active=1"
            order_info = list(db.query(sql, vars={'sid' : self.session.sid}))

            data = web.storage (
                    user  = stu_info[0],
                    order = order_info
                    )
            return render.order.orderinfo("order", U"订单信息", data)
        except Exception as err:
            return self.error(err)

    @StuAuth.sessionChecker
    def POST(self):
        pass

class get_help:
    """
    订餐帮助
    """
    def GET(self):
        return render.order.orderhelp("order", U"订餐帮助")
    def POST(self):
        pass
