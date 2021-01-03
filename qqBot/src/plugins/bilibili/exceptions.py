#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@编写人: 小蓝同学
@文件功能: 自定义异常
每天都要开心:)
"""


class BaseBilibiliException(Exception):
    def __init__(self, code, msg, url, method, params, data):
        self.code = code  # 错误码
        self.msg = msg  # 错误消息
        self.url = url  # 出错的url
        self.method = method  # 出错的请求方法
        self.params = params  # 出错请求的get参数
        self.data = data  # 出错请求的post数据


class BilibiliException(BaseBilibiliException):
    def __str__(self):
        return f'api错误' \
               f'错误码: {self.code}\t信息: {self.msg}' \
               f'出错url: {self.url}\t请求方法: {self.method}' \
               f'出错get参数: {self.params}\n出错post数据: {self.data}'


class NetworkException(Exception):
    def __init__(self, code, url, method, params, data):
        self.code = code  # 错误码
        self.url = url  # 出错的url
        self.method = method  # 出错的请求方法
        self.params = params  # 出错请求的get参数
        self.data = data  # 出错请求的post数据

    def __str__(self):
        return f'网络错误' \
               f'错误码: {self.code}\t' \
               f'出错url: {self.url}\t请求方法: {self.method}' \
               f'出错get参数: {self.params}\n出错post数据: {self.data}'
