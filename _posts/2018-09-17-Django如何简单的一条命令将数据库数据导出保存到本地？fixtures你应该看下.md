---
layout:     post
title:      Django如何简单的一条命令将数据库数据导出保存到本地？fixtures你应该看下
subtitle:   fixtures的使用
date:       2018-09-17
author:     ChrisChou
header-img: img/post-bg-coffee.jpeg
catalog: true
tags:
    - Python
    - Django
---

    在日常开发中，有的时候需要将数据库的测试数据导出来再另一台机器上运行，你可能会选择写一个导出数据的自定义命令将数据库数据导出为Excel表的形式，再在另一台机器上测试数据的时候再将Excel的数据导入到数据库中，这样会比较麻烦。可能你认为是十几行或者几十行代码的事情，但是我这个人就是懒啊，十几行的代码我也不想写。

    于是我就想，Django是出了名的便利，里面集成了很多的工具和功能，不需要再重复造轮子了，你说有没有可能这个轮子已经造好了呢，于是我就找啊找，巧了，我找到一个关键字fixtures，据说是Django自带的（我目前使用的Django版本是2.0）然后我去官方文档上翻，最后在官方的wiki上找到了它的定义

![](https://oscimg.oschina.net/oscnet/f1bba702fa96a2bf7d747ec4c7347828e71.jpg)

里面讲述到fixtures在你的应用测试期间提供了非常方便的将数据库数据导入保存在本地文件中，在需要测试的时候，再将本地数据导入到数据库中。

首先你的在你的设置中设置好你要讲app models中对应的数据导出的文件路径

```python
FIXTURE_DIRS = (
   os.path.join(BASE_DIR, 'your_app/fixtures/'),
)
```

这是我项目中的列子，我把app中的数据全部倒出到app/fixtures/下面

设置好路径之后我们再执行下面的命令将app/models中对应的数据导入到相应的路径下面

python manage.py dumpdata --format=json item > your_app/fixtures/data.json

我们来看下这个命令，dumpdata是Django manage自带的命令， --format=json 是定义数据导出到文件的格式为json数据形式，>后面的是导入的路径以及保存的文件名.

这个时候就会将数据保存到本地。。

其保存的数据格式是这样的

```
[{"model": "item.brands", "pk": 204, "fields": {"cn_name": "\u6d77\u5916\u8d2d\u54c1\u724c", "cn_name_abridge": null, "en_name": null, "form_country": null, "key_word": null, "brand_about": null, "photo_id": null, "status": "normal"}}, {"model": "item.brands", "pk": 205, "fields": {"cn_name": "\u67cf\u7433", "cn_name_abridge": null, "en_name": null, "form_country": null, "key_word": null, "brand_about": null, "photo_id": null, "status": "normal"}}, {"model": "item.brands", "pk": 206, "fields": {"cn_name": "\u4f18\u8d1d\u65bd", "cn_name_abridge": null, "en_name": null, "form_country": null, "key_word": null, "brand_about": null, "photo_id": null, "status": "normal"}}, {"model": "item.brands", "pk": 207, "fields": {"cn_name": "\u4e1d\u5854\u8299", "cn_name_abridge": null, "en_name": null, "form_country": null, "key_word": null, "brand_about": null, "photo_id": null, "status": "normal"}}, {"model": "item.brands", "pk": 208, "fields": {"cn_name": "\u4e49\u4e4c\u91c7\u8d2d", "cn_name_abridge": null, "en_name": null, "form_country": null, "key_word": null, "brand_about": null, "photo_id": null, "status": "normal"}}, {"model": "item.brands", "pk": 209, "fields": {"cn_name": "2080", "cn_name_abridge": null, "en_name": null, "form_country": null, "key_word": null, "brand_about": null, "photo_id": null, "status": "normal"}}, {"model": "item.brands", "pk": 210, "fields": {"cn_name": "\u6fb3\u6d322N", "cn_name_abridge": null, "en_name": null, "form_country": null, "key_word": null, "brand_about": null, "photo_id": null, "status": "normal"}}, {"model": "item.brands", "pk": 211, "fields": {"cn_name": "3CE", "cn_name_abridge": null, "en_name": null, "form_country": null, "key_word": null, "brand_about": null, "photo_id": null, "status": "normal"}}, {"model": "item.brands", "pk": 212, "fields": {"cn_name": "\u82f1\u56fdAA\u7f51", "cn_name_abridge": null, "en_name": null, "form_country": null, "key_word": null, "brand_about": null, "photo_id": null, "status": "normal"}}, {"model": "item.brands", "pk": 213, "fields": {"cn_name": "\u96c5\u6f3e", "cn_name_abridge": null, "en_name": null, "form_country": null, "key_word": null, "brand_about": null, "photo_id": null, "status": "normal"}}, {"model": "item.brands", "pk": 214, "fields": {"cn_name": "BASS", "cn_name_abridge": null, "en_name": null, "form_country": null, "key_word": null, "brand_about": null, "photo_id": null, "status": "normal"}}, {"model": "item.brands", "pk": 215, "fields": {"cn_name": "\u8d1d\u89c8\u5f97", "cn_name_abridge": null, "en_name": null, "form_country": null, "key_word": null, "brand_about": null, "photo_id": null, "status": "normal"}}, {"model": "item.brands", "pk": 216, "fields": {"cn_name": "MICCOSMO", "cn_name_abridge": null, "en_name": null, "form_country": null, "key_word": null, "brand_about": null, "photo_id": null, "status": "normal"}}, {"model": "item.brands", "pk": 217, "fields": {"cn_name": "cure\u9177\u96c5", "cn_name_abridge": null, "en_name": null, "form_country": null, "key_word": null, "brand_about": null, "photo_id": null, "status": "normal"}}, {"model": "item.brands", "pk": 218, "fields": {"cn_name": "\u7a00\u62c9\u514b\u513f", "cn_name_abridge": null, "en_name": null, "form_country": null, "key_word": null, "brand_about": null, "photo_id": null, "status": "normal"}}, {"model": "item.brands", "pk": 219, "fields": {"cn_name": "\u8fea\u51ef\u745e", "cn_name_abridge": null, "en_name": null, "form_country": null, "key_word": null, "brand_about": null, "photo_id": null, "status": "normal"}}, {"model": "item.brands", "pk": 220, "fields": {"cn_name": "Dr.Cox\u8fea\u67ef\u601d", "cn_name_abridge": null, "en_name": null, "form_country": null, "key_word": null, "brand_about": null, "photo_id": null, "status": "normal"}}, {"model": "item.brands", ........
```

全是json数据格式，这些都是你数据库中的数据。你成功的将它们导出。

那么我们如何将它们再导入的数据中呢？

首先我们执行python manage.py flush命令将Django models对应的数据库中的数据全部清空。

再执行python manage.py loaddata data.json命令，这个时候Django就会遍历你settings中设置的FIXTURE_DIRS路径下面找到对应的data.json的文件将其导入到对应的models下面。

没错就是这样简单，你可能还不太理解，但是我建议你亲自试一试，才知道其便利之处。。