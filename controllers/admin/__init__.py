__author__ = "fangwentong"

__all__ = ["management_app"]

try:
    from app_manage import management_app
except ImportError:
    pass
