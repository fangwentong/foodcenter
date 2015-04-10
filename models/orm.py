#!/usr/bin/env python
# coding= utf-8

__all__ = [
    "StringField",
    "IntegerField",
    "FloatField",
    "TimeField",
    "DateField",
    "BooleanField",
    "TextField",
    "BlobField",
    "Model"
]

import logging, time
import os,sys
app_root = os.path.join(os.path.dirname(__file__), os.path.pardir)
sys.path.insert(0, app_root)             # 网站根目录加入搜索路径
from config import db
import web

class Field(object):
    '''
    Basic Field Class
    '''
    _count = 0
    def __init__(self, **kw):
        self.name = kw.get('name', None)
        self._default = kw.get('default', None)
        self.primary_key = kw.get('primary_key', False)
        self.nullable = kw.get('nullable', False)
        self.updatable = kw.get('updatable', True)
        self.auto_increment = kw.get('ai', False)
        self.insertable = kw.get('insertable', True)
        self.ddl = kw.get('ddl', '')
        self._order = Field._count
        Field._count = Field._count + 1

    @property
    def default(self):
        d = self._default
        return d() if callable(d) else d

    def __str__(self):
        s = ['<%s:%s,%s,default(%s),' % (self.__class__.__name__, self.name, self.ddl, self._default)]
        self.nullable and s.append('N')
        self.updatable and s.append('U')
        self.insertable and s.append('I')
        s.append('>')
        return ''.join(s)

class StringField(Field):
    def __init__(self, **kw):
        if not 'default' in kw:
            kw['default'] = ''
        if not 'ddl' in kw:
            kw['ddl'] = 'varchar(255)'
        super(StringField, self).__init__(**kw)

class IntegerField(Field):
    def __init__(self, **kw):
        if not 'default' in kw:
            kw['default'] = 0
        if not 'ddl' in kw:
            kw['ddl'] = 'bigint'
        super(IntegerField, self).__init__(**kw)

class FloatField(Field):
    def __init__(self, **kw):
        if not 'default' in kw:
            kw['default'] = 0.0
        if not 'ddl' in kw:
            kw['ddl'] = 'real'
        super(FloatField, self).__init__(**kw)

class BooleanField(Field):
    def __init__(self, **kw):
        if not 'default' in kw:
            kw['default'] = False
        if not 'ddl' in kw:
            kw['ddl'] = 'boolean'
        super(BooleanField, self).__init__(**kw)

class TextField(Field):
    def __init__(self, **kw):
        if not 'default' in kw:
            kw['default'] = ''
        if not 'ddl' in kw:
            kw['ddl'] = 'text'
        super(TextField, self).__init__(**kw)

class BlobField(Field):
    def __init__(self, **kw):
        if not 'default' in kw:
            kw['default'] = ''
        if not 'ddl' in kw:
            kw['ddl'] = 'blob'
        super(BlobField, self).__init__(**kw)

class TimeField(Field):
    def __init__(self, **kw):
        if not 'default' in kw:
            kw['default'] = time.strftime("%Y-%m-%d %H:%M:%S")
        if not 'ddl' in kw:
            kw['ddl'] = 'timestamp'
        super(TimeField, self).__init__(**kw)

class DateField(Field):
    def __init__(self, **kw):
        if not 'default' in kw:
            kw['default'] = time.strftime("%Y-%m-%d")
        if not 'ddl' in kw:
            kw['ddl'] = 'date'
        super(DateField, self).__init__(**kw)

class VersionField(Field):
    def __init__(self, name=None):
        super(VersionField, self).__init__(name=name, default=0, ddl='bigint')

_triggers = frozenset(['pre_insert', 'pre_update', 'pre_delete'])

def _gen_sql(table_name, mappings):
    '''
    Generate SQL sentences
    '''
    pk = None
    sql = ['-- generating SQL for %s:' % table_name, 'create table `%s` (' % table_name]
    for f in sorted(mappings.values(), lambda x, y: cmp(x._order, y._order)):
        if not hasattr(f, 'ddl'):
            raise StandardError('no ddl in field "%s".' % f.name)
        ddl = f.ddl
        nullable = f.nullable
        auto_increment = f.auto_increment
        if f.primary_key:
            pk = f.name
        statement = '  `%s` %s' % (f.name, ddl)
        statement += nullable and '' or ' not null'
        statement += auto_increment and ' auto_increment' or ''
        statement += ','
        sql.append(statement)
    sql.append('  primary key(`%s`)' % pk)
    sql.append(');')
    return '\n'.join(sql)

class ModelMetaclass(type):
    '''
    Metaclass for model objects.
    '''
    def __new__(cls, name, bases, attrs):
        # skip base Model class:
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)

        # store all subclasses info:
        if not hasattr(cls, 'subclasses'):
            cls.subclasses = {}
        if not name in cls.subclasses:
            cls.subclasses[name] = name
        else:
            logging.warning('Redefine class: %s' % name)

        logging.info('Scan ORMapping %s...' % name)
        mappings = dict()
        primary_key = None
        for k, v in attrs.iteritems():
            if isinstance(v, Field):
                if not v.name:
                    v.name = k
                logging.info('Found mapping: %s => %s' % (k, v))
                # check duplicate primary key:
                if v.primary_key:
                    if primary_key:
                        raise TypeError('Cannot define more than 1 primary key in class: %s' % name)
                    if v.updatable:
                        logging.warning('NOTE: change primary key to non-updatable.')
                        v.updatable = False
                    if v.nullable:
                        logging.warning('NOTE: change primary key to non-nullable.')
                        v.nullable = False
                    primary_key = v
                mappings[k] = v
        # check exist of primary key:
        if not primary_key:
            raise TypeError('Primary key not defined in class: %s' % name)
        for k in mappings.iterkeys():
            attrs.pop(k)
        if not '__table__' in attrs:
            attrs['__table__'] = name.lower()
        attrs['__mappings__'] = mappings
        attrs['__primary_key__'] = primary_key
        attrs['__sql__'] = lambda self: _gen_sql(attrs['__table__'], mappings)
        for trigger in _triggers:
            if not trigger in attrs:
                attrs[trigger] = None
        return type.__new__(cls, name, bases, attrs)

class Model(web.Storage):
    __metaclass__ = ModelMetaclass

    def __init__(self, *obj):
        super(Model, self).__init__(*obj)

    @classmethod
    def get(cls, pk):
        '''
        Get by primary key.
        '''
        d = list(db.query('select * from %s where %s=%s' % (cls.__table__, cls.__primary_key__.name, pk)))
        return cls(d[0]) if len(d)>0 else None

    @classmethod
    def getBy(cls, **kw):
        '''
        Get by condition
        '''
        L = []
        for k, v in kw.iteritems():
            L.append('`%s`="%s"' % (k, v))
        d = list(db.query('select * from %s where %s' % (cls.__table__, " and ".join(L))))
        return cls(d[0]) if len(d)>0 else None

    @classmethod
    def getAll(cls, **kw):
        '''
        Get All by condition
        '''
        L = []
        for k, v in kw.iteritems():
            L.append('`%s`="%s"' % (k, v))
        d = list(db.query('select * from %s where %s' % (cls.__table__, " and ".join(L))))
        return [cls(item) for item in d]

    def update(self):
        self.pre_update and self.pre_update()
        L = []
        args = []
        for k, v in self.__mappings__.iteritems():
            if v.updatable:
                if hasattr(self, k):
                    arg = getattr(self, k)
                else:
                    arg = v.default
                    setattr(self, k, arg)
                L.append('`%s`="%s"' % (k, arg))
        pk = self.__primary_key__.name
        args.append(getattr(self, pk))
        db.query('update `%s` set %s where %s=$value' % (self.__table__, ','.join(L), pk), vars={'value':args})
        return self

    def delete(self):
        self.pre_delete and self.pre_delete()
        pk = self.__primary_key__.name
        args = (getattr(self, pk), )
        db.query('delete from `%s` where `%s`=$value' % (self.__table__, pk), vars={'value':args})
        return self

    def insert(self):
        self.pre_insert and self.pre_insert()
        params = {}
        for k, v in self.__mappings__.iteritems():
            if v.insertable:
                if not hasattr(self, k):
                    setattr(self, k, v.default)
                params[v.name] = getattr(self, k)
        db.insert('%s' % self.__table__, **params)
        return self

