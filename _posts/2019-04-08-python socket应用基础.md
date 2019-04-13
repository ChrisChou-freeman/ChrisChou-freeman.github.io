---
layout:     post
title:      python socket应用基础
subtitle:   socket基础
date:       2019-04-06
author:     ChrisChou
header-img: img/post-bg-coffee.jpeg
catalog: true
tags:
    - Python
    - Socket
---


socket通常也称作"套接字"，用于描述IP地址和端口，是一个通信链的句柄，应用程序通常通过"套接字"向网络发出请求或者应答网络请求。

socket起源于Unix，而Unix/Linux基本哲学之一就是“一切皆文件”，对于文件用【打开】【读写】【关闭】模式来操作。socket就是该模式的一个实现，socket即是一种特殊的文件，一些socket函数就是对其进行的操作（读/写IO、打开、关闭）

**Socket与http连接的关系**

我们在传输数据时，可以只使用（传输层）TCP/IP协议，但是那样的话，如果没有应用层，便无法识别数据内容，如果想要使传输的数据有意义，则必须使用到应用层协议，应用层协议有很多，比如HTTP、FTP、TELNET等，也可以自己定义应用层协议。WEB使用HTTP协议作应用层协议，以封装HTTP文本信息，然后使用TCP/IP做传输层协议将它发到网络上。

Socket是一个针对TCP和UDP编程的接口，你可以借助它建立TCP连接等等。而TCP和UDP协议属于传输层 。而http是个应用层的协议，它实际上也建立在TCP协议之上。Socket是对TCP/IP协议的封装，Socket本身并不是协议，而是一个调用接口（API），通过Socket，我们才能使用TCP/IP协议。Socket的出现只是使得程序员更方便地使用TCP/IP协议栈而已，是对TCP/IP协议的抽象，从而形成了我们知道的一些最基本的函数接口。

TCP连接的三次握手图示：

![](https://raw.githubusercontent.com/chrischou2018/chrischou2018.github.io/master/img/post-bg-socket.png)

**什么是****TCP****连接的三次握手？**

第一次握手：客户端发送syn包(syn=j)到服务器，并进入SYN_SEND状态，等待服务器确认；  
第二次握手：服务器收到syn包，必须确认客户的SYN（ack=j+1），同时自己也发送一个SYN包（syn=k），即SYN+ACK包，此时服务器进入SYN_RECV状态；  
第三次握手：客户端收到服务器的SYN＋ACK包，向服务器发送确认包ACK(ack=k+1)，此包发送完毕，客户端和服务器进入ESTABLISHED状态，完成三次握手。

握手过程中传送的包里不包含数据，三次握手完毕后，客户端与服务器才正式开始传送数据。理想状态下，TCP连接一旦建立，在通信双方中的任何一方主动关闭连接之前，TCP 连接都将被一直保持下去。断开连接时服务器和客户端均可以主动发起断开TCP连接的请求，断开过程需要经过“四次握手”

**socket python实例**

_socket server_

```python
import socket

ip_port = ("127.0.0.1",8888)

sk = socket.socket()
sk.bind(ip_port)
sk.listen(5)

while True:
    print("服务开启...")
    conn,addr = sk.accept()
    client_data = conn.recv(1024).decode("utf8")
    print(client_data)
    conn.sendall(bytes("你已连接成功。", encoding="utf8"))
    conn.close()
```

_socket client_

```python
import socket
ip_port = ("127.0.0.1",8888)

sk = socket.socket()
sk.connect(ip_port)
sk.sendall(bytes("请求连接", encoding="utf8"))
server_reply = sk.recv(1024).decode("utf8")
print(server_reply)
sk.close()

```

_web服务原型_

```python
import socket
 
def handle_request(client):
    buf = client.recv(1024)
    client.send(bytes("HTTP/1.1 200 OK\r\n\r\n", encoding="utf-8"))
    client.send(bytes("Hello, World", encoding="utf-8"))
 
def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost',8080))
    sock.listen(5)
    while True:
        connection, address = sock.accept()
        handle_request(connection)
        connection.close()
 
if __name__ == '__main__':
  main()
```

**sk = socket.socket(参数1,参数2,参数3)**

参数一：地址簇

　　socket.AF_INET IPv4（默认）  
　　socket.AF_INET6 IPv6

　　socket.AF_UNIX 只能够用于单一的Unix系统进程间通信

参数二：类型

　　socket.SOCK_STREAM　　流式socket , for TCP （默认）  
　　socket.SOCK_DGRAM　　 数据报式socket , for UDP

　　socket.SOCK\_RAW 原始套接字，普通的套接字无法处理ICMP、IGMP等网络报文，而SOCK\_RAW可以；其次，SOCK\_RAW也可以处理特殊的IPv4报文；此外，利用原始套接字，可以通过IP\_HDRINCL套接字选项由用户构造IP头。  
　　socket.SOCK\_RDM 是一种可靠的UDP形式，即保证交付数据报但不保证顺序。SOCK\_RAM用来提供对原始协议的低级访问，在需要执行某些特殊操作时使用，如发送ICMP报文。SOCK_RAM通常仅限于高级用户或管理员运行的程序使用。  
　　socket.SOCK_SEQPACKET 可靠的连续数据包服务

参数三：协议

　　0　　（默认）与特定的地址家族相关的协议,如果是 0 ，则系统就会根据地址格式和套接类别,自动选择一个合适的协议

**常用方法介绍**

**sk.bind(address)**

　　s.bind(address) 将套接字绑定到地址。address地址的格式取决于地址族。在AF_INET下，以元组（host,port）的形式表示地址。

**sk.listen(backlog)**

　　开始监听传入连接。backlog指定在拒绝连接之前，可以挂起的最大连接数量。

      backlog等于5，表示内核已经接到了连接请求，但服务器还没有调用accept进行处理的连接个数最大为5  
      这个值不能无限大，因为要在内核中维护连接队列

**sk.setblocking(bool)**

　　是否阻塞（默认True），如果设置False，那么accept和recv时一旦无数据，则报错。

**sk.accept()**

　　接受连接并返回（conn,address）,其中conn是新的套接字对象，可以用来接收和发送数据。address是连接客户端的地址。

　　接收TCP 客户的连接（阻塞式）等待连接的到来

**sk.connect(address)**

　　连接到address处的套接字。一般，address的格式为元组（hostname,port）,如果连接出错，返回socket.error错误。

**sk.connect_ex(address)**

　　同上，只不过会有返回值，连接成功时返回 0 ，连接失败时候返回编码，例如：10061

**sk.close()**

　　关闭套接字

**sk.recv(bufsize\[,flag\])**

　　接受套接字的数据。数据以字符串形式返回，bufsize指定**最多**可以接收的数量。flag提供有关消息的其他信息，通常可以忽略。

**sk.recvfrom(bufsize\[.flag\])**

　　与recv()类似，但返回值是（data,address）。其中data是包含接收数据的字符串，address是发送数据的套接字地址。

**sk.send(string\[,flag\])**

　　将string中的数据发送到连接的套接字。返回值是要发送的字节数量，该数量可能小于string的字节大小。即：可能未将指定内容全部发送。

**sk.sendall(string\[,flag\])**

　　将string中的数据发送到连接的套接字，但在返回之前会尝试发送所有数据。成功返回None，失败则抛出异常。

      内部通过递归调用send，将所有内容发送出去。

**sk.sendto(string\[,flag\],address)**

　　将数据发送到套接字，address是形式为（ipaddr，port）的元组，指定远程地址。返回值是发送的字节数。该函数主要用于UDP协议。

**sk.settimeout(timeout)**

　　设置套接字操作的超时期，timeout是一个浮点数，单位是秒。值为None表示没有超时期。一般，超时期应该在刚创建套接字时设置，因为它们可能用于连接的操作（如 client 连接最多等待5s ）

**sk.getpeername()**

　　返回连接套接字的远程地址。返回值通常是元组（ipaddr,port）。

**sk.getsockname()**

　　返回套接字自己的地址。通常是一个元组(ipaddr,port)

**sk.fileno()**

　　套接字的文件描述符

上面的参数介绍中我们提到了UDP连接，什么是UDP连接呢？

TCP是面向链接的，虽然说网络的不安全不稳定特性决定了多少次握手都不能保证连接的可靠性，但TCP的三次握手在最低限度上（实际上也很大程度上保证了）保证了连接的可靠性；而UDP不是面向连接的，UDP传送数据前并不与对方建立连接，对接收到的数据也不发送确认信号，发送端不知道数据是否会正确接收，当然也不用重发，所以说UDP是无连接的、不可靠的一种数据传输协议。DP的开销更小数据传输速率更高，因为不必进行收发数据的确认，所以UDP的实时性更好

我们见过的使用场景，一般TCP用于文件传输协议，而UDP则用于即时通信如QQ

**UDP实例：**

**server端**

```python
import socket
ip_port = ("127.0.0.1",8888)
sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
sk.bind(ip_port)

while True:
    print("connect preparing。。。")
    data,(host,port) = sk.recvfrom(1024)
    print(data.decode("utf-8"),host,port)
    sk.sendto(bytes("IP:{0},you are just send one message.".format(host), encoding='utf-8'), (host,port))
```

**client端**

```python
import socket
ip_port = ("127.0.0.1",8888)

sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
while True:
    inp = input("DATA：").strip()
    if inp == 'exit':
        break
    sk.sendto(bytes(inp, encoding='utf-8'),ip_port)
    data,(host,port) = sk.recvfrom(1024)
    print(data.decode("utf-8"))

sk.close()
```