---
layout:     post
title:      python socket应用进阶配合select模块IO多路复用
subtitle:   socket基础
date:       2019-04-13
author:     ChrisChou
header-img: img/post-bg-coffee.jpeg
catalog: true
tags:
    - Python
    - Socket
    - Select
---


Python中有一个select模块，其中提供了：select、poll、epoll三个方法，分别调用系统的 select，poll，epoll 从而实现IO多路复用。

Windows Python：

    提供： select

Mac Python：

    提供： select

Linux Python：

    提供： select、poll、epoll

**select**

select最早于1983年出现在4.2BSD中，它通过一个select()系统调用来监视多个文件描述符的数组，当select()返回后，该数组中就绪的文件描述符便会被内核修改标志位，使得进程可以获得这些文件描述符从而进行后续的读写操作。

select目前几乎在所有的平台上支持，其良好跨平台支持也是它的一个优点，事实上从现在看来，这也是它所剩不多的优点之一。

select的一个缺点在于单个进程能够监视的文件描述符的数量存在最大限制，在Linux上一般为1024，不过可以通过修改宏定义甚至重新编译内核的方式提升这一限制。

另外，select()所维护的存储大量文件描述符的数据结构，随着文件描述符数量的增大，其复制的开销也线性增长。同时，由于网络响应时间的延迟使得大量TCP连接处于非活跃状态，但调用select()会对所有socket进行一次线性扫描，所以这也浪费了一定的开销。

**poll**

poll在1986年诞生于System V Release 3，它和select在本质上没有多大差别，但是poll没有最大文件描述符数量的限制。

poll和select同样存在一个缺点就是，包含大量文件描述符的数组被整体复制于用户态和内核的地址空间之间，而不论这些文件描述符是否就绪，它的开销随着文件描述符数量的增加而线性增大。

另外，select()和poll()将就绪的文件描述符告诉进程后，如果进程没有对其进行IO操作，那么下次调用select()和poll()的时候将再次报告这些文件描述符，所以它们一般不会丢失就绪的消息，这种方式称为水平触发（Level Triggered）。

**epoll**

直到Linux2.6才出现了由内核直接支持的实现方法，那就是epoll，它几乎具备了之前所说的一切优点，被公认为Linux2.6下性能最好的多路I/O就绪通知方法。

epoll可以同时支持水平触发和边缘触发（Edge Triggered，只告诉进程哪些文件描述符刚刚变为就绪状态，它只说一遍，如果我们没有采取行动，那么它将不会再次告知，这种方式称为边缘触发），理论上边缘触发的性能要更高一些，但是代码实现相当复杂。

epoll同样只告知那些就绪的文件描述符，而且当我们调用epoll_wait()获得就绪文件描述符时，返回的不是实际的描述符，而是一个代表就绪描述符数量的值，你只需要去epoll指定的一个数组中依次取得相应数量的文件描述符即可，这里也使用了内存映射（mmap）技术，这样便彻底省掉了这些文件描述符在系统调用时复制的开销。

另一个本质的改进在于epoll采用基于事件的就绪通知方式。在select/poll中，进程只有在调用一定的方法后，内核才对所有监视的文件描述符进行扫描，而epoll事先通过epoll\_ctl()来注册一个文件描述符，一旦基于某个文件描述符就绪时，内核会采用类似callback的回调机制，迅速激活这个文件描述符，当进程调用epoll\_wait()时便得到通知。

## 关于select模块的select方法

返回值1, 返回值2, 返回值3 = select.select(参数1, 参数2, 参数3, 超时时间)

参数： 可接受四个参数（前三个必须）

返回值：三个列表

select方法用来监视文件句柄，如果句柄发生变化，则获取该句柄。

1、当 参数1 序列中的句柄发生可读时（accetp和read），则获取发生变化的句柄并添加到 返回值1 序列中

2、当 参数2 序列中含有句柄时，则将该序列中所有的句柄添加到 返回值2 序列中

3、当 参数3 序列中的句柄发生错误时，则将该发生错误的句柄添加到 返回值3 序列中

4、当 超时时间 未设置，则select会一直阻塞，直到监听的句柄发生变化

当 超时时间 ＝ 1时，那么如果监听的句柄均无任何变化，则select会阻塞 1 秒，之后返回三个空列表，如果监听的句柄有变化，则直接执行。

## socket server 端简单实例

```python
import socket
import select

sk1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sk1.bind(('127.0.0.1',8002))
sk1.listen(5)
sk1.setblocking(0)

inputs = [sk1,]

while True:
    readable_list, writeable_list, error_list = select.select(inputs, [], inputs, 1)
    for r in readable_list:
        # 当客户端第连接服务端时为可读socket对象
        if sk1 == r:
            # 当可读取对象为socket对象的时候，将其转变为可接受对象再放入到inputs中
            print('accept...')
            request, address = r.accept()
            应为accept的时候会阻塞，所以setblocking(0)可以让设置其为非阻塞状态
            request.setblocking(0)
            inputs.append(request)
        # 当客户端连接上服务端之后，再次发送数据时
        else:
            # 当对象为可接受对象的时候接收数据，
            received = r.recv(1024)
            # 当正常接收客户端发送的数据时
            if received:
                print('received data:', received.decode("utf-8"))
            # 当客户端关闭程序时移除对象
            else:
                inputs.remove(r)

sk1.close()
```

## socket client 端简单实例

```python
import socket

ip_port = ('127.0.0.1',8002)
sk = socket.socket()
sk.connect(ip_port)

while True:
    input_str = input('wait input:')
    sk.sendall(input_str.encode("utf-8"))
sk.close()
```

接下来部署一个socket聊天室.

## socket补充

通常情况下声明了socket之后可以对 socket进行配置选项

关于设置socket选项setsocketopt

setsockopt(level,optname,value)

**level**：

定义了哪个选项将被使用。通常情况下是SOL_SOCKET，意思是正在使用的socket选项。

它还可以通过设置一个特殊协议号码来设置协议选项，然而对于一个给定的操作系统，

大多数协议选项都是明确的，所以为了简便，它们很少用于为移动设备设计的应用程序。

**optname：**

参数提供使用的特殊选项。关于可用选项的设置，会因为操作系统的不同而有少许不同。

如果level选定了SOL_SOCKET，那么一些常用的选项

参数如下：

| 选项    | 意义    | 期望值 |
| :------: | :------: | :------: |
| SO_BINDTODEVICE | 可以使socket只在某个特殊的网络接口（网卡）有效。也许不能是移动便携设备 | 一个字符串给出设备的名称或者一个空字符串返回默认值 |
| SO_BROADCAST | 允许广播地址发送和接收信息包。只对UDP有效。如何发送和接收广播信息包 | 布尔型整数 |
| SO_DONTROUTE | 禁止通过路由器和网关往外发送信息包。这主要是为了安全而用在以太网上UDP通信的一种方法。不管目的地址使用什么IP地址，都可以防止数据离开本地网络 | 布尔型整数 |
| SO_KEEPALIVE | 可以使TCP通信的信息包保持连续性。这些信息包可以在没有信息传输的时候，使通信的双方确定连接是保持的 | 布尔型整数 |
| SO_OOBINLINE | 可以把收到的不正常数据看成是正常的数据，也就是说会通过一个标准的对recv()的调用来接收这些数据 | 布尔型整数 |
| SO_REUSEADDR | 当socket关闭后，本地端用于该socket的端口号立刻就可以被重用。通常来说，只有经过系统定义一段时间后，才能被重用。 | 布尔型整数 |

下面用到了SO_REUSEADDR选项，具体写法是：

S.setsockopt(socket.SOL\_SOCKET,socket.SO\_REUSEADDR,1) 这里value设置为1，表示将SO_REUSEADDR标记为TRUE，操作系统会在服务器socket被关闭或服务器进程终止后马上释放该服务器的端口，否则操作系统会保留几分钟该端口。

**socket客户端实例**：

```python
'''
 服务器的实现 采用select的方式
'''
import select
import socket
import sys
import queue

#创建套接字并设置该套接字为非阻塞模式

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.setblocking(0)

#绑定套接字
server_address = ('localhost',10000)
print('starting up on %s port %s'% server_address)
server.bind(server_address)

#将该socket变成服务模式
#backlog等于5，表示内核已经接到了连接请求，但服务器还没有调用accept进行处理的连接个数最大为5
#这个值不能无限大，因为要在内核中维护连接队列

server.listen(5)

#初始化读取数据的监听列表,最开始时希望从server这个套接字上读取数据
inputs = [server]

#初始化写入数据的监听列表，最开始并没有客户端连接进来，所以列表为空

outputs = []

#要发往客户端的数据
message_queues = {}
while inputs:
    print('waiting for the next event')
    #调用select监听所有监听列表中的套接字，并将准备好的套接字加入到对应的列表中
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
    #监控文件句柄有某一处发生了变化 可写 可读  异常属于Linux中的网络编程 
    #属于同步I/O操作，属于I/O复用模型的一种
    #rlist--等待到准备好读
    #wlist--等待到准备好写
    #xlist--等待到一种异常
    #处理可读取的套接字

    '''
    如果server这个套接字可读，则说明有新链接到来
    此时在server套接字上调用accept,生成一个与客户端通讯的套接字
    并将与客户端通讯的套接字加入inputs列表，下一次可以通过select检查连接是否可读
    然后在发往客户端的缓冲中加入一项，键名为:与客户端通讯的套接字，键值为空队列
    select系统调用是用来让我们的程序监视多个文件句柄(file descrīptor)的状态变化的。程序会停在select这里等待，
    直到被监视的文件句柄有某一个或多个发生了状态改变
    

    若可读的套接字不是server套接字,有两种情况:一种是有数据到来，另一种是链接断开
    如果有数据到来,先接收数据,然后将收到的数据填入往客户端的缓存区中的对应位置，最后
    将于客户端通讯的套接字加入到写数据的监听列表:
    如果套接字可读.但没有接收到数据，则说明客户端已经断开。这时需要关闭与客户端连接的套接字
    进行资源清理
    '''
        
    for s in readable: 
        if s is server:
            connection,client_address = s.accept()
            print('connection from',client_address)
            connection.setblocking(0)#设置非阻塞
            inputs.append(connection)
            message_queues[connection] = queue.Queue()
        else:
            data = s.recv(1024)
            if data:
                print('received "%s" from %s'% (data,s.getpeername()))
                message_queues[s].put(data)
                if s not in outputs:
                    outputs.append(s)
            else:
                print('closing',client_address)
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_queues[s]
                    
    #处理可写的套接字
    '''
        在发送缓冲区中取出响应的数据，发往客户端。
        如果没有数据需要写，则将套接字从发送队列中移除，select中不再监视
        '''

    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()

        except queue.Empty:
            print('  ',s.getpeername(),'queue empty')
            outputs.remove(s)
        else:
            print('sending "%s" to %s'%(next_msg,s.getpeername()))
            s.send(next_msg)



    #处理异常情况

    for s in exceptional:
        for s in exceptional:
            print('exception condition on',s.getpeername())
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]
```

**socket client 端实例：**

```python
import socket
import sys
import select

ip_port = ('127.0.0.1',10000)
sk = socket.socket()
sk.connect(ip_port)

rlist = [sys.stdin, sk]

while True:
    read_list, write_list, error_list = select.select(rlist , [], [])
    for sock in read_list:
        #incoming message from remote server
        if sock == sk:
            data = sock.recv(4096).decode("utf-8")
            if not data:
                print('\nDisconnected from chat server')
                sys.exit()
            else :
                #print data
                print("server_message:",data)
            
        #user entered a message
        elif sys.stdin in read_list :
            msg = sys.stdin.readline()
            sk.send(msg.encode("utf-8"))
sk.close()
```

## 实现socket异步聊天客户端和服务端

**server：**

```python
# Tcp Chat server
 
import socket, select
 
def broadcast_data (sock, message):
    # 用于发送消息的函数
    message = message.encode("utf-8")
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # 如果出现错误则断开连接并从连接池中删除
                socket.close()
                CONNECTION_LIST.remove(socket)
 
if __name__ == "__main__":
    CONNECTION_LIST = []
    RECV_BUFFER = 4096
    PORT = 8002
    HOST = '127.0.0.1'
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    CONNECTION_LIST.append(server_socket)
 
    print("Chat server started on port " + str(PORT))
 
    while True:
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])
        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print("Client (%s, %s) connected" % addr)
                broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)
             
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    data = data.decode("utf-8")
                    if data:
                        broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)                
                 
                except:
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print("Client (%s, %s) is offline" % addr)
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
     
    server_socket.close()
```

**client：**

```python
# Tcp Chat Client

import socket, select, string, sys
 
def prompt() :
    print('<You>', end="")
    sys.stdout.flush()
 
if __name__ == "__main__":
     
    host = '127.0.0.1'
    port = 8002
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    try :
        s.connect((host, port))
    except Exception as e:
        print('Unable to connect:', e)
        sys.exit()
     
    print('Connected to remote host. Start sending messages')
    prompt()
    rlist = [sys.stdin, s]
    while True:
        read_list, write_list, error_list = select.select(rlist , [], [])
         
        for sock in read_list:
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print('\nDisconnected from chat server')
                    sys.exit()
                else :
                    print(data.decode("utf-8"), end="")
                    prompt()
             
            else :
                msg = sys.stdin.readline()
                msg = msg.encode("utf-8")
                s.send(msg)
                prompt()
```