#!/usr/local/env python2
#coding=utf-8

import web
import hashlib, json
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
        AdminAuth.__init__(self, "admin", "管理员登陆 - 哈工大饮食中心")

    # 切莫添加sessionChecker, 否则包含循环重定向
    def GET(self):
        return render.admin.login(self.page)

    def POST(self):
        data = web.input(remeber="")   #username password remeber
        #print data

        try:
            sql = "SELECT * FROM foodcenter_admins WHERE username=$username AND password=$password"
            result = list(db.query(sql, vars={'username' : data.username, 'password' : hashlib.new("md5", data.password).hexdigest()}))

            if len(result) <= 0:    #身份验证失败
                self.page.errinfo = "您输入的用户名和密码不匹配，请检查后重试."
                print self.page.errinfo
                return render.admin.login(self.page)
            else:
                self.session.name     = result[0].username
                self.session.nickname = result[0].nickname
                self.session.role     = "admin"
                self.session.logged   = True
                if data.remeber:      #记住密码
                    web.config.session_parameters['ignore_expiry'] = True
                raise web.seeother("/dashboard")

        except Exception as err:
            self.page.title   = "出错啦!"
            self.page.errinfo  = err
            return render.errinfo(self.page)


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
        AdminAuth.__init__(self, "profile", "个人资料")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.profiles(self.page, self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        data = web.input() #nickname email ..
        try:
            db.update('foodcenter_admins', web.db.sqlwhere({'username' : self.session.name}),
                    nickname = data.nickname, email = data.email)

            self.page.successinfo = "个人资料更新成功"
            return render.admin.profiles(self.page, self.session)
        except Exception as err:
            self.page.errinfo = "出现以下错误:\n"+err
            return render.admin.profiles(self.page, self.session)


class ChgPasswd(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "setting", "设置")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.settings(self.page, self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        data = web.input(req='')
        req = data.req

        if req == "check":
            try:
                sql = "SELECT * FROM foodcenter_admins WHERE username=$username AND password=$password"
                result = list(db.query(sql, vars={'username' : self.session.name,
                    'password' : hashlib.new("md5", data.oldp).hexdigest()}))

                web.header('Content-Type', 'application/json')
                if len(result) > 0:
                    return json.dumps({'is_valid' : '1'})
                else:
                    return json.dumps({'is_valid' : '0'})
            except Exception as err:
                web.header('Content-Type', 'application/json')
                return json.dumps({'errinfo' : '出现错误: ' + err})

        elif req == "submit":
            try:
                sql = "SELECT * FROM foodcenter_admins WHERE username=$username AND password=$password"
                result = list(db.query(sql, vars={'username' : self.session.name,
                    'password' : hashlib.new("md5", data.oldp).hexdigest()}))

                web.header('Content-Type', 'application/json')
                if len(result) <= 0: # 旧密码输错
                    return json.dumps({'errinfo': '旧密码输入错误!'})
                else: # 更新密码
                    db.update('foodcenter_admins', web.db.sqlwhere({'username' : self.session.name}),
                            password = hashlib.new("md5", data.newp).hexdigest())
                    return json.dumps({'successinfo' : '密码修改成功'})
            except Exception as err:
                web.header('Content-Type', 'application/json')
                return json.dumps({'errinfo':'出现错误: '+err})
        else:
            return web.Forbidden()


class DashBoard(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "dashboard", "仪表盘")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.dashboard(self.page, self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass

class Orderings(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "orderings", "订单管理")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.orderings(self.page, self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass

class ArticleManagement(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "articles", "文章管理")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.articles(self.page, self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass

class AddArticle(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "articles", "添加文章")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin

    @AdminAuth.sessionChecker
    def POST(self):
        pass

class GetMeals(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "meals", "套餐管理")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.meals(self.page, self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass

class AddMeal(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "meals", "添加套餐")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.meals(self.page, self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass

class Feedback(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "feedback", "反馈处理")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.feedback(self.page, self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass

class Users(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "users", "用户管理")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.users(self.page, self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass

class AddUser(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "users", "添加用户")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.users(self.page, self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass

class ToolsList(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "tools", "小工具")
    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.tools(self.page, self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass

class DrawPrize(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "draw-prize", "抽奖")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.drawprize(self.page, self.session)

    @AdminAuth.sessionChecker
    def POST():
        pass

class AddOrder(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "add-order", "添加订单")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.addordering(self.page, self.session)

    @AdminAuth.sessionChecker
    def POST():
        pass

class SearchOrder(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "search-order", "查询订单")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.searchordering(self.page, self.session)

    @AdminAuth.sessionChecker
    def POST():
        pass
