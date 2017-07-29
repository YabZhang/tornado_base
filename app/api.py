#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.index import IndexHandler
from modules.index import LoginHandler


urls = [
    (r'/', IndexHandler),
    (r'/login', LoginHandler)
]
