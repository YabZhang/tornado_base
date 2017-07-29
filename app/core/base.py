# -*- coding: utf-8 -*-

import json
import traceback

from tornado.web import RequestHandler
from tornado.web import HTTPError

from core.utils import encode_auth_token
from core.utils import decode_auth_token

__all__ = [
    'BaseHandler',
]


class JSONParseError(HTTPError):
    """ custome json parse error """
    def __init__(self, status_code, log_msg, *args, **kwargs):
        super(JSONParseError, self).__init__(status_code, log_msg or '', *args, **kwargs)


class JSONParseHandler(RequestHandler):
    """ JSON parse base handler """

    def prepare(self):
        """ before handle request """
        self.set_default_headers()
        if str(self.request.method).upper() not in ('GET', 'HEAD') and \
                'multipart/form-data' not in str(self.request.headers.get('Content-Type', '')).lower():
            try:
                body_content = self.request.body.decode('utf-8')
                if body_content:
                    self.json_args = json.loads(body_content)
                else:
                    self.json_args = {}
            except Exception as e:
                raise JSONParseError(405, 'invalid json args') from e

    def write_error(self, status_code, **kwargs):
        """ on JSONParseError exception """
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
        else:
            response = {'status_code': status_code, 'message': self._reason}
            if kwargs.get('exc_info'):
                exception = kwargs['exc_info'][1]
                if isinstance(exception, JSONParseError):
                    response['message'] = exception.log_message
            self.set_default_headers()
            self.set_status(status_code)
            self.write(response)
        self.finish()


class FormHandler(object):
    """ handle form validation failure """
    @staticmethod
    def validation_error(self, form):
        """ raise error when form check failed """
        response = []
        for name, error in form.errors.items():
            response.append("%s: %s" % (name, error))
        raise HTTPError(415, ';'.join(response))


class BaseHandler(JSONParseHandler, FormHandler):

    def get_current_user(self):
        """ authentication """
        token = self.get_secure_cookie('auth') or self.request.headers.get('Authorization', '')
        if not token:
            return None

        user_id = decode_auth_token(token)
        if user_id:
            return user_id
        return None

    def set_json_content_type(self):
        """ set content type application/json """
        self.set_header("Content-Type", "application/json; charset=utf-8")
