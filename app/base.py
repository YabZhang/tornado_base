#!/usr/bin/env python3
# coding: utf-8

import jwt
import tornado.ioloop

from tornado.web import Application
from tornado.web import RequestHandler
from tornado.web import authenticated
from tornado.options import define, options, parse_command_line

define("host", default="127.0.0.1", type=str)
define("port", default=8989, type=int, help="server run on the given port, defautl 8989")


options = {
    'verify_signature': True,
    'verify_exp': True,
    'verify_nbf': False,
    'verify_iat': True,
    'verify_aud': False
}

class JWTERROR(Exception):
    pass

class JWTHandler(RequestHandler):
    """ handle JSON WEB TOKEN
        解析作为认证token使用
    """

    def __jwt_encode(self, payload):
        jwt_secret = self.application.settings.get("jwt_secret")
        if not jwt_secret:
            raise JWTERROR("must set jwt secret")
        return jwt.encode(payload=payload, key=jwt_secret)

    def __jwt_decode(self):

        auth = self.request.headers.get("Authentication")
        try:
            if not auth:
                raise ValueError()

            auth_items = auth.split()
            if len(auth_items) != 2 or auth_items[0] != "bearer":
                raise ValueError()

            token = auth_items[1]
            jwt_secret = self.application.settings.get('jwt_secret')
            return jwt.decode(token, jwt_secret)
        except Exception as e:
            raise JWTERROR("jwt token is invalid: %s" % auth)


class BaseHandler(JWTHandler):
    """ request handler baseclass """

    def get_current_user(self):
        auth = self.__jwt_decode()
        if auth.get("user_id"):
            return auth["user_id"]


class MainHandler(BaseHandler):
    """ main request handler """
    @authenticated
    def get(self):
        pass


class LoginHandler(BaseHandler):
    """ login request handler"""
    # TODO: json response
    def post(self):
        username = self.get_argument("username")
        passwd = self.get_argument("passwd")
        user_id = self.__check_credential(username, passwd)
        if user_id:    # user_id
            token = self.__jwt_encode({"user_id": result})
            return self.write({'msg': 'success', 'token': token})
        self.set_status(400)
        return self.write({'msg': 'failure'})

    def __check_credential(self, username, passwd):
        """ calc md5 and compare with value in db """
        pass


def main():
    parse_command_line()

    settings = {
        "debug": True,
        "xsrf_secret": True,
        "cookie_secret": "COOKIE_SECRET",
        "jwt_serret": "JWT_SECRET",
        "login_url": "/login"
    }

    app = Application(
        # urls
        [
            ("/", MainHandler),
            ("/login", LoginHandler)
        ],
        # settings
        **settings
    )

    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()