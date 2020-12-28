#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@编写人: 小蓝同学
@文件功能:
每天都要开心:)
"""
from nonebot import get_driver, on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event


from .config import Config, CITIES
from .data_source import get_weather

global_config = get_driver().config
plugin_config = Config(**global_config.dict())

weather = on_command('天气', rule=to_me(), priority=5)


@weather.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    args = str(event.message).strip()
    if args:
        state['city'] = args


@weather.got('city', prompt='你想查询哪个城市的天气呢?')
async def handle_city(bot: Bot, event: Event, state: dict):
    city = state['city']
    if city not in CITIES:
        await weather.reject('你想查询的城市暂不支持,请重新输入!')
    city_weather = await get_weather(city)
    await weather.finish(city_weather)
