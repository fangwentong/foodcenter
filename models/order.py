#!/usr/bin/env python
#coding=utf-8


from orm import Model, StringField, IntegerField, DateField, TimeField, BooleanField
from orm import db
import datetime

class Order(Model):
    """
    订单
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

    @classmethod
    def get_bewteen(cls, **kw):
        """
        获取指定时间内的订单
        """
        now = datetime.datetime.now()
        deltatime = datetime.timedelta(days = 7)
        start = kw.get('start', datetime.datetime.strftime(now-deltatime, "%Y-%m-%d"))
        end = kw.get('end', datetime.datetime.strftime(now, "%Y-%m-%d"))
        results = list(db.query('select * from %s where birthday between "%s" and "%s"' % (
            cls.__table__,  start, end)))
        return [cls(item) for item in results]

    @classmethod
    def get_offset(cls, **kw):
        """
        获取指定偏移量， 指定长度的数据.
        """
        offset = kw.get('offset', 0)
        limit  = kw.get('limit', 10)
        results = list(db.query('select * from %s order by %s asc limit %d offset %d' % (
            cls.__table__, cls.__primary_key__.name, limit, offset)))
        return [cls(item) for item in results]

if __name__ == "__main__":
    A = Order(dict(userId = "01"))
    B = Order(dict(userId = "02"))
    C = Order(dict(userId = "03"))
    D = Order(dict(userId = "04"))
    E = Order(dict(userId = "05"))

    # A.insert()
    # B.insert()
    # C.insert()
    # D.insert()
    # E.insert()
    result = Order.get_bewteen()
    print [item.userId for item in result]
