---
layout:     post
title:      Django时区管理
subtitle:   Django时区
date:       2018-09-07
author:     ChrisChou
header-img: img/post-bg-coffee.jpeg
catalog: true
tags:
    - Python
    - Django
---

    我发现上线服务器的时候Django后端接口时间不对，晚了8个小时。我有点懵逼了。我本地测试的时间都没有问题啊，都是标准北京时间。怎么会这样？后来发现我自己本地时间之所以没有问题是因为我的计算机设置了北京时区，而线上linux服务器有可能用的还是utc时间，所以出现时间有误差。OK既然知道问题就找解决办法，一开始我打算是用python来判断系统的时区再进行调整，我想了想，这种简单的东西应该Django web框架已经集成了，所以我就翻了翻官方文档。

需要现在settings.py中加入以下配置

```python
TIME_ZONE = 'Asia/Shanghai' #时区设置为上海时间

USE_TZ = True # 使用自定义时区
```

之后所有需要调用时间的地方都使用Django自带的工具

```python
from django.utils import timezone


current_time = timezone.now() #获得配置文件中设置的时区的datetime对象
```