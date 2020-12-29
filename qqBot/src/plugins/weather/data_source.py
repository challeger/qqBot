#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@编写人: 小蓝同学
@文件功能: 数据获取
每天都要开心:)
"""
from time import strftime, localtime
from httpx import AsyncClient, Response
from bs4 import BeautifulSoup

from config import HEADERS, CITIES, BASE_URL

"""
msg的格式

地区: 北京 日期: 2020-12-28
28日(今天) 阴转多云 -8~-1℃
29日(明天) 阴转多云 -8~-1℃
30日(后天) 阴转多云 -8~-1℃
31日(周四) 阴转多云 -8~-1℃
1日(周五)  阴转多云 -8~-1℃
2日(周六)  阴转多云 -8~-1℃
3日(周日)  阴转多云 -8~-1℃
"""


def parse_html(html: str, city) -> str:
    # 解析网页
    html = BeautifulSoup(html, 'lxml')
    # 获取一周的标签
    week_weather = html.find('ul', class_='t clearfix').find_all('li')
    msg = [f'地区: {city} 日期: {strftime("%Y-%m-%d", localtime())}']
    # 将每天的天气加到列表中
    for day_weather in week_weather:
        try:
            msg.append(f'{day_weather.h1.text:9} {day_weather.p.text:6} '
                       f'{day_weather.span.text}~{day_weather.i.text}')
        except (AttributeError, TypeError) as e:
            # 此处应该有日志记录
            msg.append('天气数据获取异常,请联系管理员~')
            break
    if len(msg) == 1:
        msg.append('天气数据获取异常,请联系管理员~')
    # 合成字符串返回
    return '\n'.join(msg)


async def get_weather(city: str) -> str:
    try:
        code = CITIES.get(city).get('AREAID')
    except (KeyError, TypeError) as e:
        # 此处应有日志记录
        return '天气数据获取异常,请联系管理员~'
    url = BASE_URL.format(code)
    async with AsyncClient(headers=HEADERS) as client:
        resp: Response = await client.get(url)
        msg = parse_html(resp.text, city)
    return msg
