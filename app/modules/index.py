# -*- coding: utf-8

import logging

from core.base import BaseHandler
from core.utils import encode_auth_token, passwd_encode
from schema.sql_orm import User


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
        logging.debug('username: %s, passwd: %s' % (args['username'], args['passwd']))

        if self.__validate_member(args['username'], args['passwd']):
            self.__set_cookie()
            result_info = 'Login Success!\n'
        else:
            self.set_status(401)
            result_info = 'Incorrect Account!\n'
        self.write(result_info)

    def __validate_member(self, member_id, passwd):
        self.user = self._session.query(User).get(member_id)
        if self.user and passwd_encode(passwd) == self.user.password:
            return True
        return False

    def __set_cookie(self):
        auth_token = encode_auth_token(self.user.member_id, self.user.password)
        self.set_secure_cookie('auth', auth_token)


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
