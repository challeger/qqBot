#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@编写人: 小蓝同学
@文件功能: 
每天都要开心:)
"""
from asyncio import sleep

from nonebot import get_driver, on_command
from nonebot.adapters.cqhttp import Bot, Event, MessageSegment
from nonebot.rule import to_me

from .apis.user import get_user_info, get_my_info
from .apis.search import bangumi_search
from .config import Config

global_config = get_driver().config
plugin_config = Config(**global_config.dict())

# 命令定义区
get_user_by_uid = on_command('查询用户', rule=to_me(), priority=5)
get_my_info_handle = on_command('我的信息', rule=to_me(), priority=5)

search_bangumi_handle = on_command('找番', aliases={'查找番剧', '搜索番剧'}, rule=to_me(), priority=5)


@get_user_by_uid.handle()
async def _(bot: Bot, event: Event, state: dict):
    args = str(event.message).strip()
    if args:
        state['mid'] = args


@get_user_by_uid.got('mid', prompt='请输入要查询用户的uid!')
async def handle_user_by_uid(bot: Bot, event: Event, state: dict):
    mid = state['mid']
    msg = await get_user_info(mid)
    await get_user_by_uid.finish(msg)


@get_my_info_handle.handle()
async def _(bot: Bot, event: Event, state: dict):
    msg = await get_my_info()
    await get_my_info_handle.finish(msg)


@search_bangumi_handle.handle()
async def _(bot: Bot, event: Event, state: dict):
    args = str(event.message).strip()
    if args:
        print(args)
        state['keyword'] = args


@search_bangumi_handle.got('keyword', prompt='请输入要搜索番剧的关键字!')
async def search_bangumi(bot: Bot, event: Event, state: dict):
    keyword = state['keyword']
    async for msg in bangumi_search(keyword):
        await search_bangumi_handle.send(msg)
        await sleep(1)
    await search_bangumi_handle.finish()
