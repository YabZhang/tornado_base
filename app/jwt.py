#-*- coding: utf-8 -*-

from tornado.web import RequestHandler


JWT_OPTIONS = {
    'verify_signature': True,
    'verify_exp': True,
    'verify_nbf': False,
    'verify_iat': True,
    'verify_aud': False
}

class JWTERROR(Exception):
    """ JWT Error """
    pass

class JWTHandler:
    """ JWTHandler is to handle JSON WEB TOKEN """

    def jwt_encode(self, payload):
        if not isinstance(payload, dict):
            raise JWTERROR("jwt payload must be a dict")

        jwt_secret = self.application.settings.get("jwt_secret")
        if not jwt_secret:
            raise JWTERROR("must set jwt secret: %s" % jwt_secret)

        jwt_expire = self.application.settings.get("jwt_expire")
        if jwt_expire and str(jwt_expire).isdigit():
            payload.update({"exp": int(jwt_expire + time.time())})
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
            result = jwt.decode(token, jwt_secret, **JWT_OPTIONS)
        except jwt.ExpiredSignatureError:
            self.set_status(403)
            self.finish({"msg": "jwt token has been expired"})

        except ValueError:
            self.set_status(403)
            self.finish({"msg": "jwt token is invalid: %s" % auth})

        except Exception as e:
            self.set_status(500)

        else:
            return result

        return {}