#!/usr/bin/env python
#coding=utf-8

import os, sys
import web

app_root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(app_root, 'virtualenv.bundle.zip'))
import werobot

from werobot.robot import BaseRoBot
from werobot.parser import parse_user_msg


def make_view(robot):
    """
    为一个 BaseRoBot 生成 webpy view。
    :param robot: 一个 BaseRoBot 实例。
    :return: 一个标准的 webpy view
    """
    assert isinstance(robot, BaseRoBot),\
        "RoBot should be an BaseRoBot instance."

    def werobot_view():
        data  = web.input(timestamp = "",
                nonce = "",
                signature = "",
                echostr = ""
                )
        timestamp = data.timestamp
        nonce = data.nonce
        signature = data.signature
        if not robot.check_signature(
            timestamp=timestamp,
            nonce=nonce,
            signature=signature
        ):
            return web.Forbidden()
        if web.ctx.method == "GET":
            return data.echostr
        elif web.ctx.method == "POST":
            body = data.body
            message = parse_user_msg(body)
            reply = robot.get_reply(message)
            return reply
        return web.Forbidden()

    return werobot_view
