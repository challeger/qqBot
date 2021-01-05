#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@编写人: 小蓝同学
@文件功能: 
每天都要开心:)
"""
from typing import Union

from nonebot.adapters.cqhttp import Message, MessageSegment
from ..config import API_DICT, USERINFO
from ..utils import is_login, get


@is_login
async def get_bangumi_meta_info(media_id: Union[str, int]) -> dict:
    """
    根据media_id获取对应的番剧信息
    :param media_id: 番剧id,对应url中的md_______
    :return:
    """
    url = API_DICT['bangumi']['info']['meta']
    return await get(url, params={'media_id': media_id}, cookies=USERINFO)
