#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@编写人: 小蓝同学
@文件功能: 要用到的一些工具类
每天都要开心:)
"""
from httpx import Response, AsyncClient
from .config import (
    HEADERS, USERINFO, API_DICT
)
from .exceptions import (
    BilibiliException, NetworkException
)


async def check_login():
    """
    检查是否登录成功
    请求url: http://api.bilibili.com/x/space/myinfo
    认证方式: Cookie(SESSDATA)
    获取本用户的详细信息
    :return: 已登录: True, 未登录: False
    """
    try:
        await get(API_DICT['user']['info']['my_info']['url'],
                  cookies=USERINFO)
    except (BilibiliException, NetworkException):
        return False
    return True


def is_login(f):
    """
    装饰器, 某些函数必须要登录
    :param f: 要执行的函数
    :return: 执行结果
    """
    async def wrapper(*args, **kwargs):
        if not await check_login():
            return '用户未登录!'
        return await f(*args, **kwargs)
    return wrapper


def is_ok(code):
    return 200 <= code <= 400


async def request(method: str, url: str, params=None, data=None,
                  cookies=None, headers=None, data_type: str = 'form', **kwargs):
    """
    自定义的请求函数
    使用httpx库的AsyncClient来创建请求
    :param method: 请求的方法
    :param url: 请求的url
    :param params: 请求的参数
    :param data: 请求的数据
    :param cookies: 请求的cookies
    :param headers: 请求的headers
    :param data_type: 请求的数据类型
    :param kwargs: 自定义关键字
    :return:
    """
    # 参数处理
    if not params: params = {}
    if not data: data = {}
    if not cookies: cookies = {}
    if not headers: headers = HEADERS.copy()
    if data_type.lower() == 'json': headers['Content-Type'] = 'application/json'

    # 创建请求
    async with AsyncClient(cookies=cookies, params=params, headers=headers) as client:
        resp: Response = await client.request(method, url, data=data, **kwargs)
        # 请求失败,抛出异常
        if not is_ok(resp.status_code):
            raise NetworkException(resp.status_code, url, method, params, data)

        # 没有数据,返回空
        if resp.headers.get('content-length') == 0:
            return None

        # 解析数据
        res = resp.json()
        # code不为0时说明请求发生了错误
        if res['code'] != 0:
            if 'message' in res:
                msg = res['message']
            elif 'msg' in res:
                msg = res['msg']
            else:
                msg = '请求失败,服务器未返回失败原因'
            raise BilibiliException(res['code'], msg, url, method, params, data)

        # 为0说明获取数据正常
        return res


async def get(url: str, params=None, cookies=None,
              headers=None, data_type: str = 'form',**kwargs):
    """
    封装的get请求
    :param url: 请求的url
    :param params: 请求的参数
    :param cookies: 请求的cookies
    :param headers: 请求的headers
    :param data_type: 请求的数据类型
    :param kwargs: 自定义关键字
    :return:
    """
    return await request('GET', url=url, params=params, cookies=cookies,
                         headers=headers, data_type=data_type, **kwargs)


async def post(url: str, data=None, cookies=None,
               headers=None, data_type: str = 'form', **kwargs):
    """
    封装的post请求
    :param url: 请求的url
    :param data: 请求的数据
    :param cookies: 请求的cookies
    :param headers: 请求的headers
    :param data_type: 请求的数据类型
    :param kwargs: 自定义关键字
    :return:
    """
    return await request('POST', url=url, data=data, cookies=cookies,
                         headers=headers, data_type=data_type, **kwargs)


async def delete(url, params=None, data=None, cookies=None,
                 headers=None, data_type: str = 'form', **kwargs):
    """
    封装的delete请求
    :param url: 请求的url
    :param params: 请求的参数
    :param data: 请求的数据
    :param cookies: 请求的cookies
    :param headers: 请求的headers
    :param data_type: 请求的数据类型
    :param kwargs: 自定义关键字
    :return:
    """
    return await request('DELETE', url=url, params=params, data=data,
                         cookies=cookies, headers=headers,
                         data_type=data_type, **kwargs)
