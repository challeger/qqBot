#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@编写人: 小蓝同学
@文件功能: 
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
                  'Chrome/87.0.4280.88 Safari/537.36'
}

# city.json文件所在的路径
JSON_PATH: str = __file__[:-9] + 'city.json'
# 初始化时读取json文件里的数据,转为字典格式
CITIES: dict = ujson.load(open(JSON_PATH, encoding='utf-8'))
# url模板
BASE_URL = 'http://www.weather.com.cn/weather/{}.shtml'
