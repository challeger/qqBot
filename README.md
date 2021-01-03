# qqBot
基于nonebot2实现的qq机器人

## 环境

**python: 3.8.6**

**所需库:**

nonebot2, ujson, bs4, httpx

## 项目参考

[`go-cqhttp`](https://github.com/Mrs4s/go-cqhttp): cqhttp的go语言实现,项目的基石1

[`NoneBot2`](https://github.com/nonebot/nonebot2): 基于Python实现的机器人框架,项目的基石2

[`bilibili-API-collect`](https://github.com/SocialSisterYi/bilibili-API-collect):b站api文档,实现bilibili应用的主要参考文档

## 开发日志

**2020.12.28** 完成测试模块 -- 天气数据获取, 从http://www.weather.com.cn/weather/获取对应的天气数据, 格式化后返回

**2021.01.03** 建立Bilibili应用,完成项目配置与登录验证.

封装了httpx的request方法,实现get,post,delete三个高层api.

完成了登录验证以及登录鉴权装饰器