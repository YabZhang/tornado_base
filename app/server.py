#!/usr/bin/env python3
# coding: utf-8

"""
@Author: YabZhang
@Data: 2017.5.14
"""

import tornado.ioloop
from tornado.web import Application
from tornado.options import options

from api import urls
from settings.config import load_config


def get_settings():

    return {
        'debug': True,
        'xsrf_secret': True,
        'cookie_secret': 'COOKIE_SECRET',
        'login_url': options.LOGIN_URL
    }


def main():
    load_config()
    settings = get_settings()

    app = Application(urls, **settings)
    app.listen(options.PORT)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
