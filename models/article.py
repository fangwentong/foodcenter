#!/usr/bin/env python
#coding=utf-8

from orm import Model, StringField, IntegerField, BooleanField, TimeField
from orm import db

class Article(Model):
    """
    文章
    """
    __table__ = 'foodcenter_articles'

    id         = IntegerField(primary_key=True, updatable=False, ai=True, ddl='int(15)')
    title      = StringField(ddl='varchar(100)')  # 标题
    thumbnail  = StringField(ddl='varchar(100)')  # 缩略图
    url        = StringField(ddl='varchar(256)')  # 网址
    postTime   = TimeField()                      # 发布日期
    lastModify = TimeField()                      # 上次修改
    isDraft    = BooleanField()                   # 是否为草稿
    summary    = StringField(ddl='varchar(512)')  # 摘要
    body       = StringField(ddl="varchar(10000)")# 文章内容
    visitors   = IntegerField(ddl="varchar(12)")  # 访客数

    @classmethod
    def get_lastest(cls, n):
        """
        获取最近几篇文章
        """
        results =  list(db.query('select * from %s where isDraft=False order by postTime desc limit %d' % (cls.__table__, n)))
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
    A = Article(dict(title = "First"))
    B = Article(dict(title = "Second"))
    C = Article(dict(title = "Third"))
    D = Article(dict(title = "Fourth"))

    # A.insert()
    # B.insert()
    # C.insert()
    # D.insert()
    result = Article.get_bewteen()
    print [item.title for item in result]
