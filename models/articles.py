#!/usr/bin/env python
#coding=utf-8

from orm import Model, StringField, IntegerField, BooleanField, TimeField

class Article(Model):
    """
    文章
    """
    __table__ = 'foodcenter_articles'

    id         = IntegerField(primary_key=True, nullable=False, ddl='int(15)')
    title      = StringField(ddl='varchar(100)')  # 标题
    thumbnail  = StringField(ddl='varchar(100)')  # 缩略图
    url        = StringField(ddl='varchar(256)')  # 网址
    postTime   = TimeField()                      # 发布日期
    lastModify = TimeField()                      # 上次修改
    isDraft    = BooleanField()                   # 是否为草稿
    summary    = StringField(ddl='varchar(512)')  # 摘要
    body       = StringField(ddl="varchar(10000)")# 文章内容
    visitors   = IntegerField(ddl="varchar(12)")  # 访客数

