__author__ = "fangwentong"

__all__ = ["db", "weconf", "render", "urls", "site", "admin"]

try:
    from setting import db, render, weconf, site, admin
    from urls import urls
except ImportError, err:
    print err
