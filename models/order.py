#!/usr/bin/env python2
#coding=utf-8

from config import setting
from base import StuAuth
import web, json

render = setting.render
db     = setting.db

def get_package_name(package_id):
    try:
        sql = "SELECT * FROM foodcenter_meals WHERE id=$id"
        result = list(db.query(sql, vars={'id' : str(package_id)}))
        if len(result) > 0:
            return result[0].name
        else:
            return "没有找到匹配的套餐"
    except Exception as err:
        return "出现错误: " + str(err)

def get_canteen_name(canteen_id):
    try:
        sql = "SELECT * FROM foodcenter_canteen WHERE cid=$cid"
        result = list(db.query(sql, vars={'cid' : canteen_id}))
        if len(result) > 0:
            return result[0].name
        else:
            return "没有找到匹配的餐厅"
    except Exception as err:
        return "出现错误: " + str(err)

class index(StuAuth):
    """
    订餐导航
    """
    def __init__(self):
        StuAuth.__init__(self, "order", "生日餐预定 - 哈工大饮食中心")

    @StuAuth.decoder
    def GET(self):
        return render.order.index(self.page, self.session)

    def POST(self):
        pass


class signup(StuAuth):
    """
    用户注册
    """
    def __init__(self):
        StuAuth.__init__(self, "order", "注册")

    @StuAuth.decoder
    def GET(self):
        return render.order.signup(self.page)

    def POST(self):
        user_info = web.input()

        try:                   #查数据表，判断是否注册
            sql = "SELECT * FROM foodcenter_users WHERE student_id=$sid"
            result = list(db.query(sql, vars={'sid':user_info.sid}))
        except Exception as err:
            return self.error(err)

        if len(result) >= 1: #已注册,自动跳转
            print("Already Registerd!")
            """
            TODO : 给出过渡页面,提示用户已经注册
            """
            raise web.seeother("/order/info")
        else:      #未注册
            sql = "SELECT * FROM foodcenter_students WHERE student_id=$sid AND student_name=$name"
            result = list(db.query(sql, vars={'sid':user_info.sid, 'name':user_info.name}))

            if len(result) <= 0:          #学生身份验证
                self.page.errinfo = "学生身份验证出错，请输入正确的学生信息."
                print self.page.errinfo
                return render.order.signup(self.page)

            weixinId = ""
            if hasattr(self.session, 'wid'):
                if StuAuth.isValid(self.session.wid):
                    weixinId = self.session.wid
                self.session.wid = ""
            try:      #验证通过， 插入新的表项
                db.insert('foodcenter_users',
                        student_id    = user_info.sid,
                        student_name  = user_info.name,
                        sex           = self.getSexId(user_info.sex),
                        birthday      = user_info.birthday,
                        phone         = user_info.phone,
                        short_message = user_info.message,
                        weixinId      = weixinId,
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
        StuAuth.__init__(self, "order", U"用户登录 - 哈工大饮食中心")

    @StuAuth.decoder
    def GET(self):
        return render.order.signin(self.page)

    def POST(self):
        data = web.input(req = '', sid = '', name = '')
        req = data.req
        print data

        if req == 'check':
            print "hello"
            if data.sid == '':
                return "{}"
            try:
                sql = "SELECT * FROM foodcenter_users WHERE student_id=$sid"
                result = list(db.query(sql, vars={'sid' : data.sid}))

                web.header('Content-Type', 'application/json')
                if len(result) > 0:       #是已注册的学生
                    return json.dumps({'valid' : '2'})
                else:
                    sql = "SELECT * FROM foodcenter_students WHERE student_id=$sid"
                    result = list(db.query(sql, vars={'sid' : data.sid}))

                    if len(result) > 0:   #是学生，但尚未注册
                        return json.dumps({'valid' : '1'})
                    else:
                        return json.dumps({'valid' : '0'})

            except Exception as err:
                return json.dumps({})

        elif req == 'submit':
            if data.sid == '':
                return json.dumps({'errinfo' : "请输入您的学号"})
            if data.name == '':
                return json.dumps({'errinfo' : "请输入您的姓名"})
            try:
                sql = "SELECT * FROM foodcenter_users WHERE student_id=$sid AND student_name=$name"
                result = list(db.query(sql, vars={'sid' : data.sid, 'name' : data.name}))

                if len(result) <= 0:          #学生身份验证
                    web.header('Content-Type', 'application/json')
                    return json.dumps({'errinfo' : "您输入的学号和姓名不匹配，请检查后重试."})
                else:
                    self.session.name   = result[0].student_name
                    self.session.sid    = result[0].student_id
                    self.session.role   = "student"
                    self.session.logged = True
                    return json.dumps({'successinfo' : '登陆成功，正在跳转'})

            except Exception as err:
                web.header('Content-Type', 'application/json')
                return json.dumps({'errinfo' : '出现错误: ' + err})
        else:
            return web.Forbidden()

class logout(StuAuth):
    """
    退出登陆
    """
    def __init__(self):
        StuAuth.__init__(self,"order", "退出登陆")

    @StuAuth.sessionChecker
    def GET(self):
        self.session.kill()
        return web.seeother('/order')

    @StuAuth.sessionChecker
    def POST(self):
        pass

class add_order(StuAuth):
    """
    添加订单
    """
    def __init__(self):
        StuAuth.__init__(self, "order", "添加订单")

    @StuAuth.decoder
    @StuAuth.sessionChecker
    def GET(self):
        return render.order.addorder(self.page)

    @StuAuth.sessionChecker
    def POST(self):
        data = web.data()
        req  = web.input(req='').req

        if req == 'canteen':
            try:
                sql = "SELECT cid, name FROM foodcenter_canteen WHERE location=$location"
                result = list(db.query(sql, vars={'location' : data}))

                web.header('Content-Type', 'application/json')
                return json.dumps(result)
            except Exception:
                web.header('Content-Type', 'application/json')
                return '{}'
        elif(req == 'package'):
            try:
                sql = "SELECT id, name, isactive FROM foodcenter_meals WHERE canteen=$canteen"
                result = list(db.query(sql, vars={'canteen': data}))
                web.header('Content-Type', 'application/json')
                return json.dumps(result)
            except Exception:
                web.header('Content-Type', 'application/json')
                return '{}'
        else:
            raise web.Forbidden()

class get_info(StuAuth):
    """
    获取用户信息
    """
    def __init__(self):
        StuAuth.__init__(self, "order", "订单信息")

    @StuAuth.decoder
    @StuAuth.sessionChecker
    def GET(self):
        # 获取用户信息
        try:
            sql        = "SELECT * FROM foodcenter_users WHERE student_id=$sid AND student_name=$name"
            stu_info   = list(db.query(sql, vars={'sid' : self.session.sid, 'name' : self.session.name}))
            # 获取订单信息
            sql        = "SELECT * FROM foodcenter_orders WHERE student_id=$sid AND active='1'"
            order_info = list(db.query(sql, vars={'sid' : self.session.sid}))

            for order in order_info:
                order.canteen = get_canteen_name(str(order.canteen_id))
            data = web.storage (
                    user  = stu_info[0],
                    orders = order_info
                    )
            print "hello"
            return render.order.orderinfo(self.page, data)
        except Exception as err:
            return self.error(err)

    @StuAuth.sessionChecker
    def POST(self):
        pass

class get_help(StuAuth):
    """
    订餐帮助
    """
    def __init__(self):
        StuAuth.__init__(self, "order", "订餐帮助 - 哈工大饮食中心")
    def GET(self):
        return render.order.orderhelp(self.page)
    def POST(self):
        pass
