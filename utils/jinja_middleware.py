#!/usr/bin/env python
#coding=utf-8

__all__ = ["JinjaRender"]

import os

class JinjaRender:
    """
    Rendering interface to Jinja2 Templates
    为webpy编写的简单Jinja2接口，替代官方库中的第三方版本
    Example:
        import JinjaRender
        render = JinjaRender('templates')
        render.path.hello(name='jinja2')
    """
    def __init__(self, *a, **kwargs):
        extensions = kwargs.pop('extensions', [])
        globals = kwargs.pop('globals', {})

        from jinja2 import Environment,FileSystemLoader
        self._lookup = Environment(loader=FileSystemLoader(*a, **kwargs), extensions=extensions)
        self._lookup.globals.update(globals)
        self.dirname = a[0]
        self.path = ""

    def __getattr__(self, name):
        # Assuming all templates end with .html
        if os.path.isdir(os.path.join(os.path.join(self.dirname, self.path), name)):
            self.path = os.path.join(self.path, name)
            return self
        else:
            self.path = os.path.join(self.path, name + '.html')
            try:
                t = self._lookup.get_template(self.path)
            except Exception, e:
                raise e
            finally:
                self.path = ""  # Reset
            return t.render
