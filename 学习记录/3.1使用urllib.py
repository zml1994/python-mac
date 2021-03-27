# http常用的库有urllib、httplib2、requests、treq等
# urllib有4个模块：
# request（http请求模块）
# error（异常处理模块）
# parse（提供了URL处理方法：拆分、解析、合并等）
# robotparser（主要用来识别robot文件）

# 1、urlopen（） 参数：url，data，timeout
import urllib.request  # http请求模块
import urllib.parse  # 提供了URL处理方法：拆分、解析、合并等
import urllib.error  # 异常处理模块
# 另一种导入写法
from urllib import request, parse
import socket

# response = urllib.request.urlopen('https://www.python.org') # 返回的是Response对象
# print(response.read().decode('utf-8'))  # .decode('utf-8') 编码方式
# print(type(response))   # type() 查询对象的类型

# HTTPResponse的常用方法有：
# read() 返回网页内容
# readinto()
# getheader(name)
# getheaders()
# fileno()
# 属性
# msg
# version
# status 状态码
# reason
# debuglevel
# closed

# print(response.status)  # 获取响应状态码
# print(type(response.getheaders()))  # 获取响应头，返回列表类型
# print(response.getheader('Server'))  # 通过传递一个参数，获取响应头中的Server值

# 2、urlopen的参数data
# 字节流编码（bytes类型），需要通过bytes()方法转换
# 如果传递了这个参数，请求方式将由Get变成了Post
# import urllib.parse
# data = bytes(urllib.parse.urlencode({'word': 'hello'}), encoding='utf-8')
# bytes()  该方法用来将字符串转换成bytes类型，第一个参数需要时str（字符串）类型，第二个参数指定编码格式
# urllib.parse.urlencode 用来将字典转换成str（字符串）
# response = urllib.request.urlopen('http://httpbin.org/post', data=data, timeout=0.1)
# print(response.read())


# 3、timeout 用来设置超时时间，
# 如果超过设定时间，将会抛出异常，不指定该参数，则使用全局默认时间。
# 支持HTTP、HTTPS、FTP请求

# try:
#     response = urllib.request.urlopen('http://httpbin.org/post', data=data, timeout=0.1)
# except urllib.error.URLError as e:  # as e 表示用e来简称urllib.error.URLError
#     if isinstance(e.reason, socket.timeout): # 比较获取的异常类型是否与指定的类型相符
#         # 如果要判断两个类型是否相同推荐使用 isinstance()。
#         # e.reason 获取异常原因
#         # socket.timeout 表示超时异常类型
#         print('请求超时了')
# 4、Request 事例
request = urllib.request.Request('https://python.org')  # 利用Request方法，将请求独立成一个对象
response = urllib.request.urlopen(request)  # 仍然使用urlopen发起请求,请求参数是一个Request类型的对象
print(response.read().decode('utf-8'))

# 5、Request构造参数
    # 第一个参数url，必传
    # 第二个参数data，如果要传，必须是bytes编码，如果是字典，用rullib.parse模块里的rulencode()编码转化成字符串。
    # 第三个参数headers是请求头，必须是字典
    # 第六个参数是method，字符串，用来指示请求方法Get、Post、Put等
# 构造对象写法
req = request.Request(url=url, data=data, headers=headers, metod='POST')

# headers添加方法
    # 1、headers=headers
    # 2、生成req对象后，通过req.add_header('此处是header的内容。。/')



