#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@编写人: 小蓝同学
@文件功能: 要用到的一些工具类
每天都要开心:)
"""
from httpx import Response, AsyncClient
from config import (
    HEADERS, USERINFO, API_DICT
)


async def check_login():
    """
    检查是否登录成功
    请求url: http://api.bilibili.com/x/space/myinfo
    认证方式: Cookie(SESSDATA)
    获取本用户的详细信息
    :return: 已登录: True, 未登录: False
    """
    async with AsyncClient(headers=HEADERS) as client:
        resp: Response = await client.get(
            API_DICT['user']['info']['my_info']['url'], cookies=USERINFO)
        if resp.status_code == 200:
            resp_json: dict = resp.json()
            return resp_json['code'] == 0


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


if __name__ == '__main__':
    @is_login
    async def hello():
        print('hello')

    import asyncio
    asyncio.get_event_loop().run_until_complete(hello())

