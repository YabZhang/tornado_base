# -*- coding: utf-8

# from tornado.web import RequestHandler
from core.base import BaseHandler
from tornado.web import HTTPError

class IndexHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.write({'msg': 'success', 'code': 0})

    def post(self):
        print(self.json_args, type(self.json_args))

