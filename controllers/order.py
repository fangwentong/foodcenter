#!/usr/bin/env python2
#coding=utf-8

import web, json
import datetime
import os, sys
import re
app_root = os.path.join(os.path.dirname(__file__), os.path.pardir)
sys.path.insert(0, app_root)

from config import render
from models import User, Order, Student, Canteen, Meal
from base import StuAuth


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
            self.session.name   = person.studentName
            self.session.sid    = person.studentId
            self.session.role   = "student"
            self.session.logged = True
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

            User(dict(
                studentId    = data.sid,
                studentName  = data.name,
                sex          = self.getSexId(data.sex),
                birthday     = data.birthday,
                phone        = data.phone,
                shortMessage = data.message,
                weixinId     = weixinId,
                addTime      = web.SQLLiteral("NOW()"),
                isLock       = False
            )).insert()
            self.session.name   = data.name
            self.session.sid    = data.sid
            self.session.role   = "student"
            self.session.logged = True
            return web.seeother("/order/info")

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
                    if hasattr(self.session, 'weixinId'):
                        user.weixinId = self.session.weixinId
                        user.update()
                        del self.session.weixinId
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
                meals = Meal.getAll(canteenId = data.canteen, active=1)
                result = [dict(id = item.id, name = item.name) for item in meals]
                return json.dumps(result)
            except Exception:
                return '{}'

        elif data.req == 'submit':
            # 验证数据有效性
            web.header('Content-Type', 'application/json')

            status =  self.checkMatch(data.studentId, data.studentName)
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

            # 检查 餐品是否有效是否有效
            meal = Meal.get(data.package)
            if meal == None or str(meal.canteenId) != str(data.canteen):
                return json.dumps({'errinfo' : "请不要伪造请求"})

            # 检查订餐日期是否有效
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', data.birthday):
                return json.dumps({'errinfo' : '请输入正确的时间!'})
            max_deltatime = datetime.timedelta(days = 7)
            min_deltatime = datetime.timedelta(days = 0)
            order_time = datetime.datetime.strptime(data.birthday, "%Y-%m-%d")
            now = datetime.datetime.now()

            # 提前 1 - 7 天订餐
            if order_time > now+max_deltatime or order_time < now + min_deltatime:
                return json.dumps({'errinfo' : '请提前1-7天订餐!'})

            user = User.getBy(studentId = data.studentId, studentName = data.studentName)
            if user.lastOrderTime:
                last_order_time = datetime.datetime.strptime(user.lastOrderTime, "%Y-%m-%d")
                deltatime = datetime.timedelta(days = 300)
                # 判断订餐间隔
                if last_order_time + deltatime > datetime.datetime.now():
                    return json.dumps({'errinfo': "订餐时间间隔过短， 一年内只能免费订餐一次!"})

            Order(dict(userId = user.id,
                canteenId = data.canteen,
                mealId = data.package,
                studentId = data.studentId,
                studentName = data.studentName,
                phone = data.phone,
                sex = self.getSexId(data.sex),
                birthday = data.birthday,
                token = self.generateToken(),
                wish = data.message,
                addTime = web.SQLLiteral("NOW()"),
                isActive = True
                )).insert()
            user.isLock = 1
            user.update()
            return json.dumps({'successinfo' : "添加成功!"})

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
                        # 之前的订单已经完成, 应该取消锁定
                        flag = 1
                        active_orders = Order.get_my_active_orders(sid)
                        for each_order in active_orders:
                            print type(each_order.birthday)
                            if datetime.datetime.strptime(str(each_order.birthday), '%Y-%m-%d') < datetime.datetime.now():
                                each_order.isActive = 0
                                each_order.update()
                            else:
                                flag = 2
                        return flag
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
                order.canteenName = Canteen.getBy(id = order.canteenId).name
                order.mealName = Meal.getBy(id = order.mealId).name
            return render.order.orderinfo(page = self.page, user = user, orders = orders)
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
