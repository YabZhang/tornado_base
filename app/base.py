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


jwt_options = {
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
        TODO: 解析作为认证token使用
    """

    def jwt_encode(self, payload):
        if not isinstance(payload, dict):
            raise JWTERROR("jwt payload must be a dict")

        jwt_secret = self.application.settings.get("jwt_secret")
        if not jwt_secret:
            raise JWTERROR("must set jwt secret: %s" % jwt_secret)

        jwt_expire = self.application.settings.get("jwt_expire")
        if jwt_expire and str(jwt_expire).isdigit():
            payload.update({"exp": int(jwt_expire)})
        return jwt.encode(payload=payload, key=jwt_secret)

    def jwt_decode(self):

        auth = self.request.headers.get("Authentication")
        try:
            if not auth:
                raise JWTERROR()

            auth_items = auth.split()
            if len(auth_items) != 2 or str(auth_items[0]).lower() != "bearer":
                raise JWTERROR()

            token = auth_items[1]
            jwt_secret = self.application.settings.get('jwt_secret')
            result = jwt.decode(token, jwt_secret, **jwt_options)
        except jwt.ExpiredSignatureError:
            self.set_status(400)
            self.finish({"msg": "jwt token has expired"})

        except ValueError:
            self.set_status(400)
            self.finish({"msg": "jwt token is invalid: %s" % auth})

        except Exception as e:
            self.set_status(500)

        else:
            return result
        return {}

class BaseHandler(JWTHandler):
    """ request handler baseclass """

    def get_current_user(self):
        jwt_auth = self.jwt_decode()
        if jwt_auth.get("user_id"):
            print(jwt_auth['user_id'])
            return jwt_auth["user_id"]


class MainHandler(BaseHandler):
    """ main request handler """
    @authenticated
    # @jsonresponse
    def get(self):
        self.write({'msg': 'success'})


class LoginHandler(BaseHandler):
    """ login request handler"""
    # TODO: json response

    # @json_response
    def post(self):
        self.set_header("content-type", "json/application")
        username = self.get_argument("username")
        passwd = self.get_argument("passwd")
        user_id = self.__check_credential(username, passwd)
        if user_id:    # user_id
            token = self.jwt_encode({"user_id": user_id})
            return self.write({'token': token.decode('utf8')})

        self.set_status(400)
        return self.write({'msg': 'user not registered'})

    def __check_credential(self, username, passwd):
        """ check user validacity and return user_id """
        if username and passwd:
            return 666    # for test


def main():
    parse_command_line()

    settings = {
        "debug": True,
        "xsrf_secret": True,
        "cookie_secret": "COOKIE_SECRET",
        "jwt_secret": "JWT_SECRET",
        "jwt_expire": 60 * 60,    # 1h
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
