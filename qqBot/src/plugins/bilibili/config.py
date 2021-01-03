#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@编写人: 小蓝同学
@文件功能: 应用配置文件
每天都要开心:)
"""
import ujson
from pydantic import BaseSettings


class Config(BaseSettings):
    plugin_settings: str = 'default'

    class Config:
        extra = 'ignore'


# 爬虫请求头
HEADERS: dict = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/87.0.4280.88 Safari/537.36',
    "Referer": "https://www.bilibili.com/"
}

# 现在文件所在的路径
now_path: str = __file__[:-9]
# 用户的信息,通过同路径下的userinfo.json读到
# userinfo.json文件所在的路径,里面保存用户的SESSDATA与BILI_JCT
USERINFO_PATH: str = now_path + 'userinfo.json'
# 初始化时读取json文件里的数据,转为字典格式
USERINFO: dict = ujson.load(open(USERINFO_PATH, encoding='utf-8'))
# api.json文件所在的路径
API_PATH: str = now_path + 'api.json'
API_DICT: dict = ujson.load(open(API_PATH, encoding='utf-8'))
