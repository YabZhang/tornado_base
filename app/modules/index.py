# -*- coding: utf-8

import logging
from core.base import BaseHandler

class IndexHandler(BaseHandler):

    def get(self):
        self.write({'msg': 'success', 'code': 0})

    def post(self):
        print(self.json_args, type(self.json_args))


class LoginHandler(BaseHandler):

    def get(self):
        """
        引导登录页面
        :return:
        """
        self.write('Please login!\n')

    def post(self):
        """
        提交登录表单
        :return:
        """
        args = self.json_args
        logging.info('username: %s, passwd: %s' % (args['username'], args['passwd']))
        self.write('username: %s, passwd: %s\n' % (args['username'], args['passwd']))

    def __validate_member_login(self, username, passwd):
        pass


class LogoutHandler(BaseHandler):

    def get(self):
        """
        退出登录，清除cookie
        :return:
        """
        pass


class ArchiveHandler(BaseHandler):

    def get(self):
        """
        获取blog列表
        :return:
        """
        pass


class ArticleHandler(BaseHandler):

    def get(self):
        """
        获取文章内容
        :return:
        """
        pass

    def post(self):
        """
        发布文章
        :return:
        """
        pass

    def put(self):
        """
        修改文章
        :return:
        """
        pass

    def delete(self):
        """
        删除文章
        :return:
        """
        pass
