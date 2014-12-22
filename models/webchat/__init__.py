# coding: utf-8
__author__ =  "fangwentong"
__all__    =  ["app_robot", "make_view"]

try:
    from robot import app_robot
    from bridge import make_view
except ImportError:
    pass
