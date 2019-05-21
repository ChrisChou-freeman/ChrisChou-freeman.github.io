---
layout:     post
title:      django使用celery整理
subtitle:   celery
date:       2019-05-19
author:     ChrisChou
header-img: img/post-bg-coffee.jpeg
catalog: true
tags:
    - Python
    - Celery
    - Django
---

上一片博客记录了如何入门级的使用celery，这里记录的是如何在Django框架中使用celery

## 快速开始
首先假设你的Django项目是这样的

```
- proj/
  - manage.py
  - proj/
    - __init__.py
    - settings.py
    - urls.py

```

然后在你的项目下面创建celery.py文件，proj/proj/celery.py，之后就可以在里面写你需要执行的task任务函数

```python
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置Django的settings目录
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

app = Celery('proj'
             broker='amqp://',
             backend='amqp://')

# 这里声明的是和celery相关的配置命名必须是以CELERY开头的,这关于上一片博客的配置方法第三种
app.config_from_object('django.conf:settings', namespace='CELERY')

# 这里声明的是自动加载所有在django settings里面注册的app下面的tasks.py
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
```

在第一行中的from \_\_future\_\_ import absolute\_import, unicode\_literals，是声明接下来的导入都是绝对路径的导入，防止在导入celery的时候出现冲突

之后就可以在你的proj/proj/\_\_init\_\_.py文件下面注册你的celery了

```python
from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)

```

上面的英文意思是这确保了你的django启动的时候celery的app对象一直被导入状态，当你使用shared\_task装饰器装饰的task函数的是就会使用这个app对象,接下来配合上面的app.autodiscover\_tasks()一起说明，上面声明了app.autodiscover_tasks会加载所有app下所有的task，假设你的目录结构如下

```python
- app1/
    - tasks.py
    - models.py
- app2/
    - tasks.py
    - models.py
```

接下来你就可以使用shared_task，在tasks.py文件中

```python
# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)
```

这个shared\_task就确保了你的\_\_init__.py下声明的celery_app就会在这里被使用，而不需要重复声明。

## 前台启动celery

```
celery worker -A proj -l info
```

## 后台启动celery

```
celery multi start w1 -A proj -l info
```

重启

```
celery  multi restart w1 -A proj -l info
```

停止

```
celery multi stop w1 -A proj -l info
```

## 补充

你除了可以用redis作为celery的代理之外还可以使用django自带的orm/cache

首先安装拓展

```
pip install django-celery-results
```

在Django设置的installed下面添加

```
INSTALLED_APPS = (
    ...,
    'django_celery_results',
)
```

执行

```
python manage.py migrate celery_results
```

如果你使用了django的settings作为celery配置文件

添加

```
CELERY_RESULT_BACKEND = 'django-db'
```

和

```
CELERY_CACHE_BACKEND = 'django-cache'
```