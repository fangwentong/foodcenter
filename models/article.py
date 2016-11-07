#!/usr/bin/env python
# coding=utf-8

from orm import Model, StringField, IntegerField, BooleanField, TimeField
from orm import db


class Article(Model):
    """
    文章
    """
    __table__ = 'hitfd_articles'

    id = IntegerField(primary_key=True, updatable=False, ai=True, ddl='int(15)')
    title = StringField(ddl='varchar(1000)')  # 标题
    thumbnail = StringField(ddl='varchar(1000)')  # 缩略图
    url = StringField(ddl='varchar(1000)')  # 网址
    lastModify = TimeField()  # 上次修改
    postTime = TimeField(ddl='datetime')  # 发布日期
    isDraft = BooleanField()  # 是否为草稿
    summary = StringField(ddl='varchar(512)')  # 摘要
    body = StringField(ddl="varchar(10000)")  # 文章内容
    visitors = IntegerField(ddl="varchar(12)")  # 访客数

    @classmethod
    def get_lastest(cls, n):
        """
        获取最近几篇文章
        """
        results = list(
            db.query('select * from %s where isDraft=False order by postTime desc limit $num' % (cls.__table__),
                     vars={'num': n}))
        return [cls(item) for item in results]

    @classmethod
    def get_offset(cls, **kw):
        """
        获取指定偏移量， 指定长度的数据.
        """
        offset = kw.get('offset', 0)
        limit = kw.get('limit', 10)
        results = list(db.query('select * from %s order by %s asc limit $limit offset $offset' % (
            cls.__table__, cls.__primary_key__.name), vars={'limit': limit, 'offset': offset}))
        return [cls(item) for item in results]


if __name__ == "__main__":
    A = Article(dict(title="First"))
    B = Article(dict(title="Second"))
    C = Article(dict(title="Third"))
    D = Article(dict(title="Fourth"))

    # A.insert()
    # B.insert()
    # C.insert()
    # D.insert()
    result = Article.get_lastest(5)
    print [item.title for item in result]
