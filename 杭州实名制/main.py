# -*- codeing = utf-8 -*-
import random
import time
import hashlib
import requests
import json
import bs4 # 网页解析，获取数据
from bs4 import BeautifulSoup
import re  # 正则表达,进行文字匹配
import urllib.request,urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作
import sqlite3  # 进行SQLite数据库操作
import org.junit.Test;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

# 1、定义主函数
def main():
    url1 = "http://115.233.209.232:9000/api/project/findProject/1/10"
    Cookie = ''
    # 1、爬去网页
    datalist = getData(baseurl)
    # savepath = "豆瓣电影Top250.xls"  # 当前文件路径下
    dbpath = "movie.db"
    # 3、保存数据
    # saveDate(datalist, savepath)\
    saveDateDB(datalist, dbpath)

# 2、获取Cookie

# 3、获取项目库数据

# 4、保存数据到excel及数据库

# 5、更新数据库数据

# 6、输出执行结果

def askUrl(url):
    # 请求头
    head = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15"
    }

    request = urllib.request.Request(url=url, headers=head)  # 封装
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


if __name__ == "__main__":  # 当程序执行时
    # 调用函数
    main()
    # init_db("movie.db")