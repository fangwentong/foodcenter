#!/usr/bin/env python
#coding=utf-8

from orm import Model, StringField, IntegerField, DateField, TimeField, BooleanField
from orm import db
from meal import Meal
from canteen import Canteen
from user import User
import web
import datetime

class Order(Model):
    """
    订单类
    """
    __table__ = 'foodcenter_orders'

    id          = IntegerField(primary_key=True, updatable=False, ai=True, ddl='int(11)')
    userId      = IntegerField(ddl='int(11)')        # 订餐人id
    canteenId   = IntegerField(ddl='int(7)')         # 就餐餐厅
    mealId      = IntegerField(ddl='int(11)')            # 套餐
    studentId   = StringField(ddl="varchar(64)")     # 就餐人学号
    studentName = StringField(ddl='varchar(255)')    # 就餐人姓名
    phone         = StringField(ddl='varchar(30)')   # 电话
    sex         = StringField(ddl='varchar(10)')     # 性别
    birthday    = DateField(ddl='date')              # 生日
    token       = IntegerField(ddl='int(6)')         # 6位 Token
    wish        = StringField(ddl='varchar(1000)')   # 生日祝福
    addTime     = TimeField()                        # 订单添加时间
    isActive    = BooleanField(default=True)         # 是否有效

    def __init__(self, *args, **kwargs):
        Model.__init__(self, *args, **kwargs)
        self.deletable = self.isActive == 1 and\
        datetime.datetime.strptime(str(self.birthday), "%Y-%m-%d") > datetime.datetime.now()

    @classmethod
    def get_bewteen(cls, **kw):
        """
        获取指定时间内的订单
        """
        now = datetime.datetime.now()
        deltatime = datetime.timedelta(days = 7)
        start = kw.get('start', datetime.datetime.strftime(now - deltatime, "%Y-%m-%d"))
        end = kw.get('end', datetime.datetime.strftime(now, "%Y-%m-%d"))
        results = list(db.query('select * from %s where birthday between "%s" and "%s"' % (
            cls.__table__,  start, end)))
        return [cls(item) for item in results]

    @classmethod
    def get_offset(cls, **kw):
        """
        获取指定偏移量， 指定长度的数据.
        """
        Order.refresh_orders() # 刷新
        offset = kw.get('offset', 0)
        limit  = kw.get('limit', 10)
        results = list(db.query('select * from %s order by %s asc limit %d offset %d' % (
            cls.__table__, cls.__primary_key__.name, limit, offset)))
        return [cls(item) for item in results]

    @classmethod
    def get_today(cls):
        """
        获取今日订单, 提供管理员查询接口
        name : 套餐名
        canteen : 领餐地点
        studentName: 领餐人姓名
        studentId:领餐人学号
        birthday: 生日
        token : 返回码
        """
        Order.refresh_orders() # 刷新
        now = datetime.datetime.now()
        orders =  cls.get_bewteen(start = datetime.datetime.strftime(now, "%Y-%m-%d"))
        return [ web.Storage(
            name        = Meal.get(each_order.mealId).name,
            canteen     = Canteen.get(each_order.canteenId).name,
            studentName = each_order.studentName,
            studentId   = each_order.studentId,
            birthday    = each_order.birthday,
            token       = each_order.token
            ) for each_order in orders]

    @classmethod
    def getAll(cls, **kw):
        """
        Override: 根据条件 获取所有订单
        """
        Order.refresh_orders() # 刷新
        L = []
        for k, v in kw.iteritems():
            L.append('`%s`="%s"' % (k, v))
        d = list(db.query('select * from %s where %s' % (cls.__table__, ' and '.join(L))))
        return [cls(item) for item in d]

    @classmethod
    def get_my_active_orders(cls, userId):
        """
        获取个人有效订单
        """
        Order.refresh_orders() # 刷新
        d = list(db.query('select * from %s where userId=%s and isActive=1 order by birthday desc' % (cls.__table__, userId)))
        return [cls(item) for item in d]

    @classmethod
    def refresh_orders(cls, **kw):
        """
        被动刷新订单信息, 更改过期订单状态，
        并同步解锁相关用户
        """
        L = ['`isActive`=1']
        for k, v in kw.iteritems():
            L.append('`%s`="%s"' % (k, v))
        active_orders = list(db.query('select * from %s where %s' % (cls.__table__, ' and '.join(L))))

        deltatime = datetime.timedelta(hours = 18)
        for each_order in active_orders:
            # 当天18:00 失效
            if datetime.datetime.strptime(str(each_order.birthday), '%Y-%m-%d')+deltatime < datetime.datetime.now():
                # 生日订餐时， 每个学号每次最多只有一个活动订单, 当该订单失效时， 解锁该用户
                user = User.getBy(studentId = each_order.studentId)
                if user != None:
                    user.isLock = 0                           # 解锁某学号用户
                    user.lastOrderTime = each_order.birthday  # 更新最后订餐时间
                    user.update()
                order = Order(each_order)
                order.isActive = 0
                order.update()

    def delete(self):
        """
        删除订单， 并解锁用户
        """
        self.pre_delete and self.pre_delete()
        pk = self.__primary_key__.name
        args = getattr(self, pk)
        db.query('delete from `%s` where `%s`=$value' % (self.__table__, pk), vars={'value':args})
        user = User.getBy(studentId = self.studentId)
        if user:
            user.isLock = 0                           # 解锁某学号用户
            user.update()

if __name__ == "__main__":
    # A = Order(dict(userId = "01"))
    # B = Order(dict(userId = "02"))
    # C = Order(dict(userId = "03"))
    # D = Order(dict(userId = "04"))
    # E = Order(dict(userId = "05"))

    # A.insert()
    # B.insert()
    # C.insert()
    # D.insert()
    # E.insert()
    result = Order.get_today()
    print [item.userId for item in result]
    print Order.get(11).deletable
