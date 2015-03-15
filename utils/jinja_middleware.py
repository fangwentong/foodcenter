#!/usr/bin/env python
#coding=utf-8

import os

class JinjaRender:
    """Rendering interface to Jinja2 Templates
    Example:
        render= render_jinja('templates')
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
            self.path = name + '.html'
            t = self._lookup.get_template(self.path)
            self.path = ""  # Rest
            return t.render

class Storage(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError, k:
            raise AttributeError, k

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttributeError, k
