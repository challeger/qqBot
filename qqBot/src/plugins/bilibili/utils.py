#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@编写人: 小蓝同学
@文件功能: 要用到的一些工具类
每天都要开心:)
"""
from httpx import Response, AsyncClient
from config import (
    HEADERS, USERINFO, CHECK_DATA, API_DICT
)


async def check_login():
    res = {}

    async with AsyncClient(headers=HEADERS) as client:
        resp: Response = await client.post(
            API_DICT['video_like'], data=CHECK_DATA,cookies=USERINFO)
        if resp.status_code == 200:
            resp_json: dict = resp.json()
            if resp_json['code'] == -111:
                res['code'] = -1
                res['message'] = 'csrf 校验失败'
            elif resp_json['code'] in (-101, -400):
                res['code'] = -2
                res['message'] = 'SESSDATA值有误'
            else:
                res['code'] = 0
                res['message'] = '0'
    return res


if __name__ == '__main__':
    import asyncio
    asyncio.get_event_loop().run_until_complete(check_login())

