import requests
from requests import HTTPError
import json
import time
import sqlite3
from sqlite封装 import get_db_conn, close_db_conn

db_file1 = 'xssmz.db'  # 数据库地址

def tongji(db_file):
    sql = '''select count(*) from Project'''
    # sql4 = '''select * from Project where ProjectID = "2bd16428-9a0a-e911-ada5-f34a08fe5ab1" '''
    sql4 = '''select count(*) from Project where ConsNo is null '''
    sql1 = '''select count(*) from Project where xsProjectCodeis = 0'''
    sql2 = '''select count(*) from Project where xsProjectCodeis = 1'''
    sql3 = '''select count(*) from Project where hzProjectCodeis = 0'''
    sql5 = '''select count(*) from Project where hzProjectCodeis = 1'''
    sql6 = '''select count(*) from Project where hzProjectCodeis = 3'''
    sql7 = '''select count(*) from Project where hzProjectCodeis = 0 and ConsUnitNameCode is null'''
    sql8 = '''select count(*) from Project where hzProjectCodeis = 0 and ShigongUnitNameCode is null'''
    conn = sqlite3.connect(db_file)  # 打开或创建数据库文件
    cur = conn.cursor()  # 创建游标
    print('数据库总计项目：%d' % caxun(cur, sql)[0][0])
    # print(caxun(cur, sql4))
    print('无施工许可证项目：%d' % caxun(cur, sql4)[0][0])
    print('    厂家未对接项目：%d' % caxun(cur, sql1)[0][0])
    print('    已分配密钥项目：%d' % caxun(cur, sql2)[0][0])
    print('\n需要添加到杭州：%d' % caxun(cur, sql3)[0][0])
    print('已添加到杭州：%d' % caxun(cur, sql5)[0][0])
    print('不需要添加到杭州：%d' % caxun(cur, sql6)[0][0])
    print('需要添加到杭州建设单位无统一社会信用代码：%d' % caxun(cur, sql7)[0][0])
    print('需要添加到杭州施工单位无统一社会信用代码：%d' % caxun(cur, sql8)[0][0])
    # aaa = cur.fetchall()
    cur.close()  # 关闭游标
    conn.close()  # 关闭数据库

def caxun(cur, sql):
    cur.execute(sql)  # 执行sql语句
    return cur.fetchall()

tongji(db_file1)