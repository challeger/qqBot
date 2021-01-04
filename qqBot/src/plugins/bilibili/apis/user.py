#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@编写人: 小蓝同学
@文件功能: 用户接口文件
每天都要开心:)
"""
from nonebot.adapters.cqhttp import Message, MessageSegment
from ..config import API_DICT, USERINFO
from ..utils import is_login, get


@is_login
async def get_user_relation_dict(mid: int) -> dict:
    """
    获取指定用户的关注数与粉丝数, 返回字典类型数据, 底层api
    :param mid: 用户的uid
    :return: 用户的关注数与粉丝数
    """
    url = API_DICT['user']['info']['relation']['url']
    return await get(url, params={'vmid': mid}, cookies=USERINFO)


@is_login
async def get_user_info_dict(mid: int) -> dict:
    """
    获取指定用户的基本信息, 返回字典类型数据, 底层api
    :param mid: 用户的uid
    :return: 用户的信息
    """
    url = API_DICT['user']['info']['info']['url']
    return await get(url, params={'mid': mid}, cookies=USERINFO)


@is_login
async def get_my_info_dict() -> dict:
    """
    获取登录用户的基本信息, 返回字典类型数据, 底层api
    :return:
    """
    url = API_DICT['user']['info']['my_info']['url']
    return await get(url, cookies=USERINFO)


# 用户信息的字符串模板
INFO_TEMPLATE = '''uid: {uid}
用户名: {name}
性别: {sex} 等级: {level}
个性签名: {sign}
认证: {official}
关注数: {following} 粉丝数: {follower}
是否关注: {is_followed}
直播间标题: {room_title}
直播间url: {room_url}
是否开播: {is_live}
-------------------------------
友利奈绪_-_  uid:129262727
点个关注吧秋梨膏~
'''


async def get_user_info(mid: int) -> Message:
    """
    获取指定用户的基本信息, 返回字符串类型数据, 提供给高层调用
    :param mid: 用户的uid
    :return:
    """
    # 基本信息的响应
    info_resp = (await get_user_info_dict(mid))['data']
    # 关注数与粉丝数的响应
    relation_resp = (await get_user_relation_dict(mid))['data']
    msg = Message(MessageSegment.image(info_resp['face']))  # 头像url
    msg.append(INFO_TEMPLATE.format(
        uid=info_resp['mid'], name=info_resp['name'],
        sex=info_resp['sex'], sign=info_resp['sign'],
        level=info_resp['level'], official=info_resp['official']['title'],
        following=relation_resp['following'],
        follower=relation_resp['follower'],
        is_followed='已关注' if info_resp['is_followed'] else '未关注',
        room_title=info_resp['live_room']['title'],
        room_url=info_resp['live_room']['url'],
        is_live='直播中' if info_resp['live_room']['liveStatus'] else '未开播'
    ))
    return msg


MY_INFO_TEMPLATE = '''uid: {uid}
用户名: {name}
性别: {sex} 等级: {level}
硬币: {coins}
个性签名: {sign}
认证: {official}
粉丝数: {follower}
-------------------------------
友利奈绪_-_  uid:129262727
点个关注吧秋梨膏~
'''


async def get_my_info() -> Message:
    """
    获取登录用户的基本信息, 返回字符串类型数据, 提供给高层调用
    :return:
    """
    resp = (await get_my_info_dict())['data']
    msg = Message(MessageSegment.image(resp['face']))  # 头像url
    msg.append(MY_INFO_TEMPLATE.format(
        uid=resp['mid'], name=resp['name'],
        sex=resp['sex'], coins=resp['coins'], sign=resp['sign'],
        level=resp['level'], official=resp['official']['title'],
        follower=resp['follower'],
    ))
    return msg
