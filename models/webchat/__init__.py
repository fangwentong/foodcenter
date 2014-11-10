__author__ =  "fangwentong"
__all__    =  ["WeixinInterface", "app_robot"]

try:
    from verify import WeixinInterface
    from robot import app_robot
except ImportError:
    pass

