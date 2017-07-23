# -*- coding: utf-8

from core.base import BaseHandler

class IndexHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.write({'msg': 'success', 'code': 0})

    def post(self):
        print(self.json_args, type(self.json_args))

