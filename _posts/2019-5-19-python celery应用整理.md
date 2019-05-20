---
layout:     post
title:      python celery 应用整理
subtitle:   celery
date:       2019-05-19
author:     ChrisChou
header-img: img/post-bg-coffee.jpeg
catalog: true
tags:
    - Python
    - Celery
---

## 什么是celery？

    什么是celery？异步转发任务至队列处理，无阻塞。这是在后端领域提高代码执行效率的一种手段。将原本可能需要花时间同步等待的函数或者叫task转发至代理执行如redis server。然后执行剩下代码，之后再请求的时候确认有没有执行完成就可，如果完成则返回执行结果，如果任务还在后台进行，则返回任务还在执行中。

redis 工作流程图

![](https://oscimg.oschina.net/oscnet/7ca6b44a5f10831ba46b9393a6e0fa081fe.jpg)

这篇博客我将阅读过的博客和官方最新文档，进行整理，以在工作中能够快速上手为目的。。

## 快速上手

首先安装celery

```
pip3 install Celery
```

因为是选择将redis作为中间代理，所以还需要安装redis server

```
sudo apt-get install redis-server
```

创建tasks.py文件

```python
from celery import Celery
 
app = Celery('tasks',
             broker='redis://localhost',
             backend='redis://localhost')
 
@app.task
def add(x,y):
    print("running...",x,y)
    return x+y
```

声明一个app的celery对象名叫tasks，add函数就是一个task用于调用执行异步任务并执行完成后返回结果

#### 启动task

启动任务之前确保redis-server已经运行

执行命令

```
celery worker -A tasks -l debug
```

worker是声明启动一个worker，-A 是指你的app的文件名， -l 是日志文件的等级log level，对应的等级还有 info、warning、error

启动后就可以在别的文件中

```python
from tasks import add
t = add.delay(3,3) #此时worker会生成一个任务和任务id
t.get() #获取任务执行的结果
result = t.get(propagate=False) #如果任务执行中出现异常,在client端不会异常退出
print(result)#结果为6
is_redy = t.ready()#查看任务是否执行完毕返回bool值
print(is_redy)
t.traceback #打印异常详细信息
```

#### 配置设置

方法一：

```
app.conf.enable_utc = True
```

方法二：

```
app.conf.update(
    enable_utc=True,
    timezone='Europe/London',
)
```

方法三：

创建一个配置文件叫celeryconfig.py

```python
from celery import Celery

app = Celery()
app.config_from_object('celeryconfig')
```

celeryconfig.py文件内容

```
enable_utc = True
timezone = 'Europe/London'
```

方法四：

创建一个配置参数的类

```python
from celery import Celery

app = Celery()

class Config:
    enable_utc = True
    timezone = 'Europe/London'

app.config_from_object(Config)
```

#### 设置环境变量：

```python
import os
from celery import Celery

#: Set default configuration module name
os.environ.setdefault('CELERY_CONFIG_MODULE', 'celeryconfig')

app = Celery()
app.config_from_envvar('CELERY_CONFIG_MODULE')
```

#### 创建定时计划任务

创建一个名为periodic_tasks.py的文件用于声明计划任务

```python
from __future__ import absolute_import, unicode_literals
from .celery import app
from celery.schedules import crontab


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # 每10秒执行一次test
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # 每30秒执行一次test
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # 每周5的晚上9点42分执行test
    sender.add_periodic_task(
        crontab(hour=21, minute=42, day_of_week=5),
        test.s('Happy Friday!'),
    )

@app.task
def test(arg):
    print(arg)
```

在app.py文件中

```python
from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('proj',
             broker='redis://localhost',
             backend='redis://localhost',
             include=['periodic_tasks'])
# include可以导入多个模块，比如这里导入了计划任务模块，你还可以单独创建一个task模块专门用来放task任务，并导入

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
```

还有更多定时配置方式如下：

| Example | Meaning |
| :------: | :------: |
| crontab() | Execute every minute. |
| crontab(minute=0, hour=0) | Execute daily at midnight. |
| crontab(minute=0, hour='*/3') | Execute every three hours: midnight, 3am, 6am, 9am, noon, 3pm, 6pm, 9pm. |
| crontab(minute=0,hour='0,3,6,9,12,15,18,21') | Same as previous. |
| crontab(minute='*/15') | Execute every 15 minutes. |
| crontab(day\_of\_week='sunday') | Execute every minute (!) at Sundays. |
| crontab(minute='*',hour='*',day\_of\_week='sun') | Same as previous. |
| crontab(minute='*/10',hour='3,17,22',day\_of\_week='thu,fri') | Execute every ten minutes, but only between 3-4 am, 5-6 pm, and 10-11 pm on Thursdays or Fridays. |
| crontab(minute=0,hour='*/2,*/3') | Execute every even hour, and every hour divisible by three. This means: at every hour _except_: 1am, 5am, 7am, 11am, 1pm, 5pm, 7pm, 11pm |
| crontab(minute=0, hour='*/5') | Execute hour divisible by 5. This means that it is triggered at 3pm, not 5pm (since 3pm equals the 24-hour clock value of “15”, which is divisible by 5). |
| crontab(minute=0, hour='*/3,8-17') | Execute every hour divisible by 3, and every hour during office hours (8am-5pm). |
| crontab(0, 0,day\_of\_month='2') | Execute on the second day of every month. |
| crontab(0, 0,day\_of\_month='2-30/3') | Execute on every even numbered day. |
| crontab(0, 0, day\_of\_month='1-7,15-21') | Execute on the first and third weeks of the month. |
| crontab(0, 0,day\_of\_month='11', month\_of\_year='5') | Execute on the eleventh of May every year. |
| crontab(0, 0,month\_of\_year='*/3') | Execute on the first month of every quarter. |