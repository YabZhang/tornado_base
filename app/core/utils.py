# -*- coding: utf-8 -*-

import logging
import base64
from hashlib import md5

from tornado.options import options, define


"""
    工具函数；    
"""


def passwd_encode(passwd):
    new_string = "{0}:{1}".format(options.AUTH_SALT, passwd)
    md5_obj = md5()
    md5_obj.update(passwd)
    return md5_obj.hexdigest()


def encode_auth_token(member_id, hashed_pwd):
    """
    加密认证口令
    :param string:
    :return:
    """
    base_str = "{salt}:{member_id}:{hashed_pwd}".format(
        salt=options.AUTH_SALT, member_id=member_id, hashed_pwd=hashed_pwd
    )
    try:
        md5_obj = md5()
        md5_obj.update(base_str.encode('utf8'))
        token = md5_obj.hexdigest()
        base = "{salt}:{member_id}:{token}".format(
            salt=options.AUTH_SALT, member_id=member_id, token=token
        )
        return base64.b64encode(base.encode('utf8')).decode()
    except Exception as e:
        logging.exception(e)
        raise e


def decode_auth_token(token):
    """
    解码认证token,并返回
    """
    salt, member_id, token = base64.b64decode(str(token).encode()).split(':')
    if not (salt and member_id and salt == options.AUTH_SALT):
        raise ValueError("Invalid User!")

    if not (token and len(token) == 32):
        raise ValueError("Invalid User!")

    return member_id, token


if __name__ == '__main__':
    define('AUTH_SALT', default='aeiou')

    member_id = 123456
    hashed_passwd = '78e78cc2cae9a'
    token = encode_auth_token(member_id, hashed_passwd)
    print(token)
    # new_member_id = 12345
    # print(decode_auth_token(token, new_member_id, hashed_passwd))
    # print(decode_auth_token(token, member_id, hashed_passwd))
