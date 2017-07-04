#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path

from tornado.options import define
from tornado.options import options
from tornado.options import parse_config_file


def load_config():
    """
    load configration
    """

    # server config
    define('DEBUG', default=True)
    define('GZIP', default=True)
    define('XHEADERS', default=True)
    define('COOKIE_SECRET', default="__DON'T_USE_THIS_OR_YOU_WILL_BE_FIRE__")
    define('XSRF_COOKIES', default="__DON'T_USE_THIS_OR_YOU_WILL_BE_FIRE__")

    # server run stat
    define('HOST', default='127.0.0.1')
    define('PORT', default=8080)
    define('PROCESS_NUM', default=1)

    # app path config
    define('AUTH_SALT', default="")
    define('LOGIN_URL', default="/login")
    define('STATIC_PATH_NAME', default="static")
    define('TEMPLATE_PATH_NAME', default="templates")

    base_path = os.path.dirname(os.path.dirname(__file__))
    define('STATIC_PATH',
           default=os.path.join(base_path, options.STATIC_PATH_NAME))
    define('TEMPLATE_PATH',
           default=os.path.join(base_path, options.TEMPLATE_PATH_NAME))

    # mysql config
    define('MYSQL', default={
        'master': 'mysql+pymysql://root:root@db_server:3306/db_name?charset=utf8',
        'slave': 'mysql+pymysql://slave:slave@db_server:3306/db_name?charset=utf8'
    })

    # mongodb config
    define('MONGO_PORT', default=27017)
    define('MONGO_HOST', default="mongo_server")

    # redis config
    define('REDIS_PORT', default=6379)
    define('REDIS_HOST', default="redis_server")

    # loading config from conf
    abs_path = os.path.abspath(__file__)
    root_path = os.path.dirname(os.path.dirname(os.path.dirname(abs_path)))
    define('ROOT_PATH', default=root_path)

    config_file = os.path.join(options.ROOT_PATH, "etc", "online.conf")
    if os.path.isfile(config_file):
        parse_config_file(config_file)


if __name__ == "__main__":
    load_config()
    print("HOST: %s, PORT: %s" % (options.HOST, options.PORT))

