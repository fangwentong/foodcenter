#!/usr/bin/env python2
# coding=utf-8

import sys, os

app_root = os.path.join(os.path.dirname(__file__), os.path.pardir)
sys.path.insert(0, app_root)
from config import setting
from base import BasePage
from models import Prize
import web, json, random
from base import StuAuth

render = setting.render


class act20151111(BasePage):
    """
    2015年双十一活动
    """

    def __init__(self):
        BasePage.__init__(self, "act20151111", U"学苑一楼自助早餐6.99元限时抢购")
        self.activity_number = '20151111'
        self.capacity = 600
        self.start_number = 4000

    def GET(self):
        cookie = web.cookies().get('foodcenter_sid')
        user = Prize.getBy(cookie=cookie, activity_number=self.activity_number)
        soldout = True if Prize.getOrderCount(self.activity_number) >= self.capacity else False
        return render.activities.act20151111(page=self.page, user=user, overflow=soldout)

    def POST(self):
        data = web.input(phone='')
        cookie = web.cookies().get('foodcenter_sid')
        web.header('Content-Type', 'application/json')
        if not data.phone:
            return json.dumps({'err': '请输入手机号码'})
        user = Prize.getBy(cookie=cookie, activity_number=self.activity_number)
        if user is None:
            user = Prize.getBy(phone=data.phone, activity_number=self.activity_number)
        if user is not None:
            user.cookie = cookie
            user.update()
            return json.dumps({'success': '已抢到'})
        else:
            if Prize.getOrderCount(self.activity_number) > self.capacity:
                return json.dumps({'success': '抱歉, 已售罄.'})
            else:
                Prize(dict(
                    phone=data.get('phone'),
                    cookie=cookie,
                    order_number=Prize.getOrderNumber(self.activity_number, self.start_number),
                    activity_number=self.activity_number,
                )).insert()
                return json.dumps({'success': '抢购成功.'})


class act20151219(BasePage):
    """
    2015年四六级活动
    """

    def __init__(self):
        BasePage.__init__(self, "act20151219", U"笑傲四六级, 能量加油早餐限时抢购")
        self.activity_number = '20151219'
        self.capacity = 189
        self.start_number = 80000

    def GET(self):
        cookie = web.cookies().get('foodcenter_sid')
        user = Prize.getBy(cookie=cookie, activity_number=self.activity_number)
        soldout = True if Prize.getOrderCount(self.activity_number) >= self.capacity else False
        if user is not None:
            user.order_desc = 'A 热狗+咖啡' if user.order_type == 1 else 'B 煎饼果子+甜奶'
        return render.activities.act20151219(page=self.page, user=user, overflow=soldout)

    def POST(self):
        data = web.input(phone='', order_type='')
        cookie = web.cookies().get('foodcenter_sid')
        web.header('Content-Type', 'application/json')
        if not data.phone:
            return json.dumps({'err': '请输入手机号码'})
        if not data.order_type:
            return json.dumps({'err': '请选择套餐类型'})
        if not data.order_type in ['1', '2']:
            return json.dumps({'err': '套餐类型无效'})
        user = Prize.getBy(cookie=cookie, activity_number=self.activity_number)
        if user is None:
            user = Prize.getBy(phone=data.phone, activity_number=self.activity_number)
        if user is not None:
            user.cookie = cookie
            user.update()
            return json.dumps({'success': '已抢到'})
        else:
            if Prize.getOrderCount(self.activity_number) > self.capacity:
                return json.dumps({'success': '抱歉, 已售罄.'})
            else:
                Prize(dict(
                    phone=data.get('phone'),
                    cookie=cookie,
                    order_number=Prize.getOrderNumber(self.activity_number, self.start_number),
                    activity_number=self.activity_number,
                    order_type=data.order_type,
                )).insert()
                return json.dumps({'success': '抢购成功.'})


class act20160308(BasePage):
    """
    2016年国际妇女节活动
    """

    def __init__(self):
        BasePage.__init__(self, "act20160308", U"娘娘节美食展1-9折优惠券领取")
        self.activity_number = '20160308'
        self.capacity = web.Storage({
            '1': 20,
            '6': 50,
            '8': 2147483647,
        })

    def GET(self):
        data = web.input(wid='')
        if not hasattr(self.session, 'weixinId'):
            if StuAuth.isValid(data.wid):
                self.session.weixinId = data.wid
                return web.seeother("")
            else:
                self.page.errinfo = '请关注哈工大饮食中心微信公众账号, 输入"娘娘节"'
                return render.errinfo(page=self.page)
        weixinId = self.session.get('weixinId')
        user = Prize.getBy(weixinId=weixinId, activity_number=self.activity_number)
        print user
        return render.activities.act20160308(page=self.page, user=user)

    def POST(self):
        data = web.input(req='')
        web.header('Content-Type', 'application/json')

        if not hasattr(self.session, 'weixinId'):
            return json.dumps({'err': '请关注哈工大饮食中心微信公众账号, 输入"娘娘节"'})
        user = Prize.getBy(weixinId=self.session.get('weixinId'), activity_number=self.activity_number)
        if data.req == 'get_code':
            if user != None:
                return json.dumps({'err': '您已经抽到奖品.'})
            # return json.dumps({'err': '未到开奖时间'})
            code = self.get_code()
            Prize(dict(
                weixinId=self.session.get('weixinId'),
                activity_number=self.activity_number,
                order_type=code,
            )).insert()
            return json.dumps({'success': '成功抢到', 'item': code})
        if data.req == 'use':
            if user is None:
                return json.dumps({'err': '您尚未抽奖!'})
            if user.is_used == 1:
                return json.dumps({'err': '您已经用过啦!'})
            user.is_used = 1
            user.update()
            return json.dumps({'success': '使用成功!'})

    # 抽奖逻辑, 只返回 1, 6, 8
    def get_code(self):
        countByType = web.storage()
        for _ in Prize.getOrderCountByType(activity_number=self.activity_number): countByType[_.order_type] = int(
            _.order_count)
        rand = random.randint(1, 10)
        if rand == 1 and (countByType.get(1) == None or countByType.get(1) < self.capacity.get('1')):
            return 1
        elif rand in [2, 3] and (countByType.get(6) == None or countByType.get(6) < self.capacity.get('6')):
            return 6
        else:
            return 8


class update():
    def GET(self):
        l = Prize.getAll(number=4000)
        start = 4022
        for _ in l:
            start += 1
            _.number = str(start)
            _.update()
        return str(start)
