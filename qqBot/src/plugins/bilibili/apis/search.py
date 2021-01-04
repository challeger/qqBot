#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@编写人: 小蓝同学
@文件功能: 搜索api
每天都要开心:)
"""
from typing import Union

from nonebot.adapters.cqhttp import Message, MessageSegment
from ..config import API_DICT, USERINFO
from ..utils import is_login, get


async def type_search(search_type: str, keyword: str, **kwargs) -> dict:
    """
    分类搜索的底层api
    :param search_type: 搜索的类别
    :param keyword: 搜索的关键字
    :param kwargs: 其余关键字,详情参考api文档
    :return: 字典类型的数据
    """
    url = API_DICT['search']['type_search']['url']
    kwargs.update({'search_type': search_type,
                   'keyword': keyword})
    return await get(url, params=kwargs, cookies=USERINFO)


async def bangumi_search_dict(keyword: str, order: str, page: int) -> dict:
    """
    番剧搜索, 底层api
    :param keyword: 搜索的关键字
    :param order: 结果排序方式,默认是综合排序
    :param page: 页码,默认是第1页
    :return: 字典类型的数据
    """
    return await type_search(search_type='media_bangumi', keyword=keyword, order=order, page=page)


BANGUMI_SEARCH_RES = '''番剧id: {media_id}
番名: {title}
地区: {areas}
风格: {styles}
番剧简介: {desc}
番剧评分: {score}分 by {user_count}人
看番传送门: {goto_url}
总集数: {ep_count}
是否需要会员: {is_vip}
'''


async def bangumi_search(keyword, order: str = 'totalrank', count: int = 5):
    """
    番剧搜索, 返回msg, 给高层使用
    暂时只返回前5个番剧, 后续考虑优化成搜索任意数量的番剧
    :param keyword: 关键字
    :param order: 排序方式,默认是综合排序
    :param count: 获取的番剧数量
    :return:
    """
    resp = (await bangumi_search_dict(keyword, order, 1))['data']
    # 0表示没有找到结果
    if resp['numResults'] == 0:
        yield '搜索的关键字没有结果呢!换一个结果吧~'

    for item in resp['result'][:count]:
        msg = Message()
        # 是否需要会员
        flag = '否'
        # 番剧标题
        title = item['title'].replace('<em class="keyword">', '').replace('</em>', '')
        # 评分
        score, user_count = '暂无评分', '暂无评分'
        if item['media_score']:
            score, user_count = item['media_score']['score'], item['media_score']['user_count']
        # 判断番剧是否需要会员
        for info in item['display_info']:
            if info['text'] == '会员专享':
                flag = '是'
                break
        # 番剧的信息
        msg.append(MessageSegment.text(BANGUMI_SEARCH_RES.format(
            media_id=item['media_id'], title=title, areas=item['areas'],
            styles=item['styles'], desc=item['desc'], score=score,
            user_count=user_count, goto_url=item['goto_url'],
            ep_count=len(item['eps']), is_vip=flag
        )))
        # 番剧的封面图片
        msg.append(MessageSegment.image(item['cover']))
        yield msg
