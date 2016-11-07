#!/usr/bin/env python
# coding=utf-8

from orm import Model, StringField, IntegerField, BooleanField, TimeField
from orm import db
import web, datetime


class FeedBack(Model):
    """
    反馈
    """
    __table__ = 'hitfd_feedbacks'

    id = IntegerField(primary_key=True, ddl='int(11)', ai=True, updatable=False)
    name = StringField(ddl='varchar(255)')  # 用户名
    email = StringField(ddl="varchar(128)")  # 邮箱
    phone = StringField(ddl='varchar(30)')  # 电话
    content = StringField(ddl='varchar(2500)')  # 反馈内容
    solved = BooleanField(default=False)  # 是否解决
    addTime = TimeField()  # 添加时间

    def get_all_feedback_by_page(start, size):
        pass

    def get_unhandle_feedback_by_page(start, size):
        pass

    @classmethod
    def get_bewteen(cls, **kw):
        """
        获取指定时间内的订单
        """
        now = datetime.datetime.now()
        deltatime = datetime.timedelta(days=0)
        start = kw.get('start', datetime.datetime.strftime(now - deltatime, "%Y-%m-%d"))
        end = kw.get('end', datetime.datetime.strftime(now, "%Y-%m-%d"))
        offset = kw.get('offset', 0)
        limit = kw.get('limit', 100)
        if kw.has_key('limit'):
            results = list(db.query('select * from %s where addTime between $start and $end'
                                    ' order by addTime desc limit $limit offset $offset' % cls.__table__,
                                    vars={'start': start, 'end': end, 'limit': limit, 'offset': offset}))
        else:
            results = list(db.query('select * from %s where addTime between $start and $end order by addTime desc' % (
                cls.__table__), vars={'start': start, 'end': end}))
        return [web.Storage(
            id=each_feedback.id,
            name=each_feedback.name,
            email=each_feedback.email,
            phone=each_feedback.phone,
            content=each_feedback.content,
            solved=each_feedback.solved,
            addTime=each_feedback.addTime,
        ) for each_feedback in results]
