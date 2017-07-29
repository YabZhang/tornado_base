# -*- coding: utf-8 -*-

import logging
from hashlib import md5

from tornado.options import options

"""
    工具函数；    
"""


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
    except Exception as e:
        logging.exception(e)
        raise e

    return token


def decode_auth_token(token, member_id, hashed_pwd):
    """
    解码认证token,并返回用户id
    １．validate auth token;
    2. get user id
    :param token:
    :return:
    """
    if not (token and len(token) == 32):
        return 0
    print(hashed_passwd, hashed_pwd)
    reproduced = encode_auth_token(member_id, hashed_pwd)
    print(reproduced, token)
    if reproduced == token:
        return member_id
    return 0


if __name__ == '__main__':
    member_id = 123456
    hashed_passwd = '78e78cc2cae9a'
    token = encode_auth_token(member_id, hashed_passwd)
    new_member_id = 12345
    print(decode_auth_token(token, new_member_id, hashed_passwd))
    print(decode_auth_token(token, member_id, hashed_passwd))
