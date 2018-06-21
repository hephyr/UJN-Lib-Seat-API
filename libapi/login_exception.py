#!/usr/bin/env python
# encoding: utf-8


class LoginException(Exception):
    def __init__(self, account, password, message):
        err = '登录异常:账号:%s 密码:%s %s' % (account, password, message)
        Exception.__init__(self, err)
        self.err = err
        self.account = account
        self.password = password
        self.message = message
