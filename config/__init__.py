__author__ = "fangwentong`"

__all__ = ["db", "weconf", "render", "urls"]

try:
    from setting import db, weconf, render
    from urls import urls
except ImportError, err:
    print err
