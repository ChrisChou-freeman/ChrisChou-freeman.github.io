---
layout:     post
title:      手写一个tornado框架session功能
subtitle:   session的实现
date:       2019-04-01
author:     ChrisChou
header-img: img/post-bg-coffee.jpeg
catalog: true
tags:
    - Python
    - Tornado
---

在web开发的时候因为我们经常需要用到cookie来识别和保存用户状态，但是cookie又不是很安全，很多信息直接明文就暴露了，这个时候session就派上用场了，而python web框架tornado就没有自带的session功能，这个时候我自己手撸一个出来，其实了解session的原理的话还是很好写的。

什么是session？

我们知道因为http连接是无状态的，客户端连接服务器请求完数据后便断开连接，下一次连接的时候服务器端便不知道你是谁，那么服务器要通过怎样知道你是谁呢，这个时候就需要cookie了，cookie等于是一个身份令牌，当你来请求服务器端的时候，服务器端会给客户端发一个令牌，而客户端下一次访问的时候，就可以带着这个令牌来访问服务端。这就是cookie的原理。打个比方当你通过账户密码登陆网站的时候，服务端就会往你的cookie里面写入，is\_login=true, user\_id=1这种方式来记录用户已经登陆。当你带着这个 cookie去访问服务端的时候，服务端就知道你已经登陆了，并且你是用户1。但是这种方式太简单粗暴了，不太安全。我们应该保证这类令牌是随机的不可预料性以保证其最基本的安全。

    了解cookie原理后再来看session原理，既然session可以解决安全等问题，他是如何做到呢？既然cookie将一些敏感数据简单粗暴的存储在客户端这样不安全，那session就是将数据存储在服务器端以便每次认证，并每次都会更新。

照着这个思路我们来看看代码部分

这里假设你已经完成了登陆功能，并创建了用户表。

首先在用户模型中添加一个字段（我的tornado项目用的model模块是peewee）

```python
sessions            = peewee.CharField(db_column="sessions")
```

看看登陆是怎么处理的

```python
        # 假设前面完成用户账户密码认证并获取到用户对象member_obj（从用户表中获取到的用户对象）
        # 生成10位的随机字符串
        sess_key = ''.join(
            random.choice(string.ascii_lowercase + string.digits) \
            for i in range(10)
        )
        # 将其保存到字典中
        session = {"id": sess_key, "time": int(time.time())}
        try:
        # 从用户表中读取存入的json数据并将其从json转为列表
            sessions = json.loads(member_obj.sessions)
        except:
            sessions = list()
        if not isinstance(sessions, list):
            sessions = list()
        # 将当前生成session key字典加入sessions list
        # 限制session list长度为5
        sessions.append(session)
        if len(sessions) > 5:
            sessions = sessions[-5:]
        将session list转为json存入用户表中的session列中
        member_obj.sessions = json.dumps(sessions)
        member_obj.save()
        # 将其写入cookie中，以便从cookie中获取数据后对其进行认证（这里其实暴露了member_id你可以对cookie value二次加密，我偷懒就没弄）
        self.set_cookie(self.settings["cookie_key_sess"],
            str(member_obj.member_id)+":"+sess_key
        )
```

然后我们可以对tornado的 RequestHandler的get\_current\_user进行重写（这是tornado用于用户认证预留的钩子函数，详细可以看官方文档）

```python
    def get_current_user(self):
        cookie_data = self.get_cookie(self.settings["cookie_key_sess"])
        if not cookie_data:
            return None

        try:
            telephone, session_id = cookie_data.split(":")
        except:
            return None
        #这个是我自己写的Member model下的classmethod
        member = Member.get_user_by_sess(member_id, session_id)
        return member


#Member model下的classmethod

   @classmethod
    def get_user_by_sess(cls, member_id, session_id):
        member = None
        sessions = None
        try:
            member = cls.get(
                (cls.member_id == member_id) & (cls.status == 'normal') #status是用户状态，判断是否被注销
            )
            sessions = json.loads(member.sessions)
        except:
            return None

        if not member or not sessions or not isinstance(sessions, list):
            return None

        for session in sessions: #判断用户携带过来的session数据是否有效，有效返回member对象
            if isinstance(session, dict) and session.get("id") \
                    and session["id"] == session_id:
                return member
        return None
```