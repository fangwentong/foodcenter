#!/usr/local/env python2
#coding=utf-8

import web
import hashlib, json
import sys, os
app_root = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)
sys.path.insert(0, app_root)

from config import render
from Auth import AdminAuth
from models import Admin, Order, Canteen, FeedBack, Meal, Order

class Index(AdminAuth):
    """
    主页, 重定向值Dashboard
    """
    def __init__(self):
        AdminAuth.__init__(self)

    @AdminAuth.sessionChecker
    def GET(self):
        raise web.seeother('/dashboard')

    @AdminAuth.sessionChecker
    def POST(self):
        pass

class LogIn(AdminAuth):
    """
    管理员登陆
    """
    def __init__(self):
        AdminAuth.__init__(self, "admin", "管理员登陆 - 哈工大饮食中心")

    # 切莫添加sessionChecker, 否则包含循环重定向
    def GET(self):
        return render.admin.login(page = self.page)

    def POST(self):
        # username password remeber
        data = web.input(username = "", password = "", remeber = "")
        try:
            result = Admin.getBy(
                username = data.username,
                password = hashlib.new("md5", data.password).hexdigest()
                )

            if result == None:    #身份验证失败
                # self.page.errinfo = "您输入的用户名和密码不匹配，请检查后重试."
                # print self.page.errinfo
                # return render.admin.login(page = self.page)
                return json.dumps({'err': '您输入的用户名和密码不匹配，请检查后重试'})
            else:
                self.session.username     = result.username
                self.session.nickname = result.nickname
                self.session.role     = "admin"
                self.session.logged   = True
                if data.remeber:      #记住密码
                    web.config.session_parameters['ignore_expiry'] = True
                return json.dumps({'success': '登录成功!'})

        except Exception as err:
            self.page.title   = "出错啦!"
            self.page.errinfo  = err
            return render.errinfo(page = self.page)


class LogOut(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self)

    @AdminAuth.sessionChecker
    def GET(self):
        self.session.kill()
        return web.seeother('/')


class GetProfile(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "profile", "个人资料")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.profiles(page = self.page, session = self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        data = web.input(req='')
        req = data.req

        if req == "email":
            try:
                result = Admin.getBy(username = self.session.username)
                web.header('Content-Type', 'application/json')
                if result:
                    return json.dumps({'email' : result.email})
                else:
                    return json.dumps({'err' : '没有找到匹配的用户'})
            except Exception as err:
                web.header('Content-Type', 'application/json')
                return json.dumps({'err' : '出现错误: ' + str(err)})

        elif req == "submit":
            web.header('Content-Type', 'application/json')
            try:
                if data.nickname == "":
                    return json.dumps({"err", "请输入昵称"})
                if data.email == "email":
                    return json.dumps({'err', "请输入邮箱"})

                person = Admin.getBy(username = self.session.username)
                person.nickname = data.nickname
                person.email = data.email
                person.update()

                self.session.nickname = data.nickname
                return json.dumps({'success': "个人资料更新成功"})
            except Exception as err:
                return json.dumps({'err' : "出现错误: " + str(err)})
        else:
            return web.Forbidden()


class ChgPasswd(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "setting", "设置")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.settings(page = self.page, session = self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        data = web.input(req='')
        req = data.req

        if req == "check":
            try:
                person = Admin.getBy(
                    username = self.session.username,
                    password = hashlib.new("md5", data.oldp).hexdigest()
                )

                web.header('Content-Type', 'application/json')
                if person:
                    return json.dumps({'is_valid' : '1'})
                else:
                    return json.dumps({'is_valid' : '0'})
            except Exception as err:
                web.header('Content-Type', 'application/json')
                return json.dumps({'err' : '出现错误: ' + str(err)})

        elif req == "submit":
            try:
                person = Admin.getBy(
                    username = self.session.username,
                    password = hashlib.new("md5", data.oldp).hexdigest()
                )
                web.header('Content-Type', 'application/json')
                if person == None: # 旧密码输错
                    return json.dumps({'err': '旧密码输入错误!'})
                else: # 更新密码
                    person.password = hashlib.new("md5", data.newp).hexdigest()
                    person.update()
                    return json.dumps({'success' : '密码修改成功'})
            except Exception as err:
                web.header('Content-Type', 'application/json')
                return json.dumps({'err':'出现错误: '+ str(err)})
        else:
            return web.Forbidden()


class DashBoard(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "dashboard", "仪表盘")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.dashboard(page = self.page, session = self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass


class Orderings(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "orderings", "订单管理")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.orderings(page = self.page, session = self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass


class ArticleManagement(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "articles", "文章管理")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.articles(page = self.page, session = self.session)

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
        return render.admin.meals(page = self.page, session = self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass


class AddMeal(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "meals", "添加套餐")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.meals(page = self.page, session = self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass


class Feedback(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "feedback", "反馈处理")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.feedback(page = self.page, session = self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass


class Users(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "users", "用户管理")

    @AdminAuth.sessionChecker
    def GET(self):
        admins = Admin.getAll()
        operator = Admin.getBy(username = self.session.username)
        print admins
        for i in range(len(admins)): # role = 0 为最高权限， role越大， 权限越低
            if admins[i].username == operator.username:
                index = i
            admins[i].deletable = (admins[i].role > operator.role)
        admins.pop(index)
        print admins
        return render.admin.users(page = self.page, session = self.session, admins = admins)

    @AdminAuth.sessionChecker
    def POST(self):
        data = web.input(req='', username = '', id='', newp='')
        req = data.req

        if req == 'check':
            try:
                person = Admin.getBy(username = data.username)
                web.header('Content-Type', 'application/json')
                if person == None:
                    return json.dumps({'is_valid' : '1'})
                else:
                    return json.dumps({'is_valid' : '0'})
            except Exception as err:
                web.header('Content-Type', 'application/json')
                raise err
                return json.dumps({'err' : '出现错误: ' + str(err)})

        elif req == 'submit':
            try:
                person = Admin.getBy(username = data.username)
                web.header('Content-Type', 'application/json')
                if person: # 用户名已被占用
                    return json.dumps({'err': '用户名已被占用!'})
                else: # 更新密码
                    Admin(dict(
                        username = data.username,
                        password = hashlib.new('md5', data.newp).hexdigest(),
                        role  = data.role,
                    )).insert()
                    return json.dumps({'success' : '成功添加用户'})
            except Exception as err:
                web.header('Content-Type', 'application/json')
                return json.dumps({'err':'出现错误: '+ str(err)})

        elif req == 'delete':
            if not data.id:
                return json.dumps({'err': '请求出错'})
            person = Admin.get(data.id)
            operator = Admin.getBy(username = self.session.username)
            if not person:
                return json.dumps({'err': '用户不存在'})
            if operator.role >= person.role:
                return json.dumps({'err': '无权限'})
            person.delete()
            return json.dumps({'success': '已删除'})

        elif req == 'update':
            person = Admin.getBy(username = data.username)
            operator = Admin.getBy(username = self.session.username)
            if not person:
                return json.dumps({'err': '用户不存在'})
            if operator.role >= person.role:
                return json.dumps({'err': '无权限'})
            person.password =  hashlib.new('md5', data.newp).hexdigest()
            person.update()
            return json.dumps({'success': '修改成功!'})
        else:
            return web.Forbidden()


class ToolsList(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "tools", "小工具")
    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.tools(page = self.page, session = self.session)

    @AdminAuth.sessionChecker
    def POST(self):
        pass


class DrawPrize(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "draw-prize", "抽奖")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.drawprize(page = self.page, session = self.session)

    @AdminAuth.sessionChecker
    def POST():
        pass


class AddOrder(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "add-order", "添加订单")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.addordering(page = self.page, session = self.session)

    @AdminAuth.sessionChecker
    def POST():
        pass


class SearchOrder(AdminAuth):
    def __init__(self):
        AdminAuth.__init__(self, "search-order", "查询订单")

    @AdminAuth.sessionChecker
    def GET(self):
        return render.admin.searchordering(page = self.page, session = self.session)

    @AdminAuth.sessionChecker
    def POST():
        pass
