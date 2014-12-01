#!/usr/local/env python2
#coding=utf-8

import web
import hashlib
from config import setting
from Auth import AdminAuth

render = setting.render
db = setting.db


class Index(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self)

    @AdminAuth.sessionChecker
    def GET(self):
        raise web.seeother('/dashboard')

    @AdminAuth.sessionChecker
    def POST(self):
        pass

class LogIn(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self)

    # 切莫添加sessionChecker, 否则包含循环重定向
    def GET(self):
        return render.admin.login("admin", "管理员登录", "")

    def POST(self):
        data = web.input(remeber="")   #username password remeber
        #print data

        try:
            sql = "SELECT * FROM foodcenter_admins WHERE username=$username AND password=$password"
            result = list(db.query(sql, vars={'username' : data.username, 'password' : hashlib.new("md5", data.password).hexdigest()}))

            if len(result) <= 0:    #身份验证失败
                errinfo = "您输入的用户名和密码不匹配，请检查后重试."
                print errinfo
                return render.admin.login("admin", U"管理员登录", errinfo)
            else:
                self.session.name     = result[0].username
                self.session.nickname = result[0].nickname
                self.session.role     = "admin"
                self.session.logged   = True
                if data.remeber:      #记住密码
                    web.config.session_parameters['ignore_expiry'] = True
                raise web.seeother("/dashboard")

        except Exception as err:
            return self.error(err)


class LogOut(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self)

    @AdminAuth.sessionChecker
    def GET(self):
        self.session.kill()
        return web.seeother('/')

    @AdminAuth.sessionChecker
    def POST(self):
        pass


class GetProfile(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self)

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.profiles("profile", "个人资料", self.session, "")

    @AdminAuth.sessionChecker
    def POST(self):
        data = web.input() #nickname email ..
        try:
            db.update('foodcenter_admins', web.db.sqlwhere({'username' : self.session.name}),
                    nickname = data.nickname, email = data.email)
            return render.admin.profiles("profile", "个人资料", self.session, "个人资料更新成功!", "success")
        except Exception as err:
            return render.admin.profiles("profile", "个人资料", self.session, "出现以下错误:\n"+err)


class ChgPasswd(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self)

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.settings("setting", "设置", self.session, "")

    @AdminAuth.sessionChecker
    def POST(self):
        data = web.input()   #old_passwd new_passwd
        try:
            sql = "SELECT * FROM foodcenter_admins WHERE username=$username AND password=$password"
            result = list(db.query(sql, vars={'username' : self.session.name,
                'password' : hashlib.new("md5", data.old_passwd).hexdigest()}))

            if len(result) <= 0: # 旧密码输错
                return render.admin.settings("setting", "设置",self.session, "旧密码输入错误!")
            else: # 更新密码
                db.update('foodcenter_admins', web.db.sqlwhere({'username' : self.session.name}),
                        password = hashlib.new("md5", data.new_passwd).hexdigest())
                return render.admin.settings("setting", "设置", self.session, "密码修改成功!", "success")
        except Exception as err:
            return self.error(err)

class DashBoard(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self)

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.dashboard("dashboard", "仪表盘", self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass

class Orderings(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self)

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.orderings("orderings", "订单管理", self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass

class GetMeals(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self)

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.meals("meals", "套餐管理", self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass

class AddMeal(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self)

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.meals("meals", "添加套餐", self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass

class Feedback(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self)

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.feedback("feedback", "反馈处理", self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass

class Users(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self)

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.users("users", "用户管理", self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass

class AddUser(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self)

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.users("users", "添加用户", self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass

class DrawPrize(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self)

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin

    @AdminAuth.sessionChecker
    def POST():
        pass

class AddOrder(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self)

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin

    @AdminAuth.sessionChecker
    def POST():
        pass

class SearchOrder(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self)

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin

    @AdminAuth.sessionChecker
    def POST():
        pass
