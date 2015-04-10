#!/usr/bin/env python2
#coding=utf-8

import web, json
import os, sys
app_root = os.path.join(os.path.dirname(__file__), os.path.pardir)
sys.path.insert(0, app_root)

from config import render, db
from models import User, Order, Student, Canteen, Meal
from base import StuAuth


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
        return render.order.index(page = self.page, session = self.session)



class signup(StuAuth):
    """
    用户注册
    """
    def __init__(self):
        StuAuth.__init__(self, "order", "注册")

    @StuAuth.decoder
    def GET(self):
        return render.order.signup(page = self.page)

    def POST(self):
        data = web.input(
            sid = "",
            name = "",
            birthday = "",
            phone = "",
            sex = "",
            message = ""
        )

        if data.sid:
            person = User.getBy(studentId = data.sid)

        if person:
            print("Already Registerd!")
            """
            TODO : 给出过渡页面,提示用户已经注册
            """
            raise web.seeother("/order/info")
        else:      #未注册
            student = Student.getBy(studentId = data.sid, studentName = data.name)

            if student == None:    # 学号&姓名无效
                self.page.errinfo = "学生身份验证出错，请输入正确的学生信息."
                print self.page.errinfo
                return render.order.signup(page = self.page)
            weixinId = ""
            if hasattr(self.session, 'weixinId'):
                weixinId = self.session.weixinId
                del self.session.weixinId

            try:                 # 插入新用户信息
                User(dict(
                    studentId    = data.sid,
                    studentName  = data.name,
                    sex          = self.getSexId(data.name),
                    birthday     = data.birthday,
                    phone        = data.phone,
                    shortMessage = data.message,
                    weixinId     = weixinId,
                    addTime      = web.SQLLiteral("NOW()"),
                    isLock       = False
                )).insert()
                return web.seeother("/order/info")
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
        return render.order.signin(page = self.page)

    def POST(self):
        data = web.input(req = '', sid = '', name = '')

        if data.req == 'check':
            web.header('Content-Type', 'application/json')
            if data.sid == '':
                return "{}"
            try:
                if User.getBy(studentId = data.sid):  # 是已注册的学生
                    return json.dumps({'valid' : '2'})
                else:
                    if Student.getBy(studentId = data.sid):   #是学生，但尚未注册
                        return json.dumps({'valid' : '1'})
                    else:
                        return json.dumps({'valid' : '0'})
            except Exception as err:
                return json.dumps({})

        elif data.req == 'submit':
            web.header('Content-Type', 'application/json')
            if data.sid == '':
                return json.dumps({'errinfo' : "请输入您的学号"})
            if data.name == '':
                return json.dumps({'errinfo' : "请输入您的姓名"})
            try:
                user = User.getBy(studentId = data.sid, studentName = data.name)
                if user == None:          # 学生身份验证失败
                    return json.dumps({'errinfo' : "您输入的学号和姓名不匹配，请检查后重试."})
                else:
                    self.session.name   = user.studentName
                    self.session.sid    = user.studentId
                    self.session.role   = "student"
                    self.session.logged = True
                    return json.dumps({'successinfo' : '登陆成功，正在跳转'})
            except Exception as err:
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


class add_order(StuAuth):
    """
    添加订单
    """
    def __init__(self):
        StuAuth.__init__(self, "order", "添加订单")

    @StuAuth.decoder
    @StuAuth.sessionChecker
    def GET(self):
        return render.order.addorder(page = self.page)

    @StuAuth.sessionChecker
    def POST(self):
        data = web.input(req="")

        if data.req == 'canteen':
            web.header('Content-Type', 'application/json')
            try:
                canteens = Canteen.getAll(location = data.location)
                result = [dict(cid = item.id, name = item.name) for item in canteens]
                return json.dumps(result)
            except Exception:
                return '{}'

        elif data.req == 'package':
            web.header('Content-Type', 'application/json')
            try:
                meals = Meal.getAll(canteenId = data.canteen)
                result = [dict(id = item.id, name = item.name) for item in meals]
                return json.dumps(result)
            except Exception:
                return '{}'

        elif data.req == 'submit':
            # 验证数据有效性
            web.header('Content-Type', 'application/json')
            try:
                status =  self.checkMatch(data.student_id, data.student_name)
                if status == -3:
                    return json.dumps({'errinfo' : "抱歉，系统出现错误."})
                elif status == -2:
                    return json.dumps({'errinfo' : "姓名不能为空"})
                elif status == -1:
                    return json.dumps({'errinfo' : "学号不能为空"})
                elif status == 0:
                    return json.dumps({'errinfo' : "学号与姓名不匹配!"})
                elif status == 2:
                    return json.dumps({'errinfo' : "您的账户被锁定，请检查是否您是否有未完成的订单!"})
                elif status == 3:
                    return json.dumps({'errinfo' : "此账户尚未注册，请先注册", 'action':'signup'})

                user = User.getBy(studentId = data.student_id, studentName = data.student_name)
                Order(userId = user.id,
                    canteenId = data.canteen,
                    mealId = data.package,
                    studentId = data.student_id,
                    studentName = data.student_name,
                    phone = data.phone,
                    sex = self.getSexId(data.sex),
                    birthday = data.birthday,
                    token = self.generateToken(),
                    wish = data.message,
                    addTime = web.SQLLiteral("NOW()"),
                    isActive = True
                    ).insert()
                return json.dumps({'successinfo' : "添加成功!"})
            except Exception as err:
                return json.dumps({'errinfo' : "出现错误: " + str(err)})

        else:
            raise web.Forbidden()

    def getSexId(self, sex):
        """
        根据性别名称获取性别id
        """
        if sex == "boy":
            return 0
        elif sex == "girl":
            return 1
        else:
            print ("Invalid Sex!\n")
            return -1

    def checkMatch(self, sid, name):
        if sid == '':
            return -1
        if name == '':
            return -2
        try:
            student = Student.getBy(studentId = sid, studentName = name)
            if student:  # 学生身份验证通过
                user = User.getBy(studentId = sid, studentName = name)
                if user:   # 已注册
                    if user.isLock:   # 被锁定
                        return 2
                    else:               # 有效
                        return 1
                else:      # 没有注册
                    return 3
            else:
                return 0 # 验证出错
        except Exception as err:
            print err
            return -3  # 系统出现错误

    def generateToken(self):
        return "123456"


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
            user = User.getBy(studentId = self.session.sid, studentName = self.session.name)
            # 获取订单信息
            if user == None:
                return self.error("没有找到您的信息")
            orders = Order.getAll(studentId = self.session.sid)

            for order in orders:
                order.canteen = get_canteen_name(str(order.canteen_id))
            data = web.storage (
                    user  = user,
                    orders = orders
                    )
            return render.order.orderinfo(page = self.page, data = data)
        except Exception as err:
            return self.error(err)


class get_help(StuAuth):
    """
    订餐帮助
    """
    def __init__(self):
        StuAuth.__init__(self, "order", "订餐帮助 - 哈工大饮食中心")
    def GET(self):
        return render.order.orderhelp(page = self.page)
