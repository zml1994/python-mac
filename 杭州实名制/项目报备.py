import requests
import json
import time
import sqlite3
from sqlite封装 import get_db_conn, close_db_conn
db_file1 = 'hzsmz.db'
n = 1  # 页码
m = 20
j = 100  # 每页大小


def main1(token):
    list1 = askUrl(n, j, token)
    list3 = uplist(list1, db_file1)
    if list3 == []:
        print("数据库新增数据0条")
    else:
        row = up_key(list3, db_file1)
        print("数据库新增数据%d条" % row)


# 请求 项目报备
def askUrl(i, j, token):
    url = 'http://115.233.209.232:9000/api/realname/project/register/%d/%d/findProjectRegister' % (i, j)
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-access-token': token}
    data = {}  # 空字典
    # data = json.dumps(data)   #  序列化成jsong
    r = requests.post(url=url, json=data, headers=headers)
    r.encoding = 'utf-8'
    # print(r.json())
    print("post执行状态码：%s" % r.json()['code'])
    print("post执行结果：%s" % r.json()['msg'])
    print("post本页数据总数：%s" % r.json()['data']['currentPageSize'])
    print("页码：%s" % r.json()['data']['pageNum'])
    print("每页大小：%s" % r.json()['data']['pageSize'])
    print("总共%s页" % r.json()['data']['totalPage'])
    print("项目总数总数：%s" % r.json()['data']['total'])
    data = r.json()['data']
    list1 = data['list']
    return list1


# 查询数据
def select_score_all(db_file, id):
    sql = '''select * from Project where secretKey =?
    '''
    conn = sqlite3.connect(db_file)  # 打开或创建数据库文件
    cur = conn.cursor()  # 创建游标
    cur.execute(sql, id)  # 执行sql语句
    # print(cur.fetchall())  # 打印所有结果
    aaa = cur.fetchall()
    cur.close()  # 关闭游标
    conn.close()  # 关闭数据库
    return aaa


# 构建批量插入数据的列表
def uplist(list1, db_file1):
    list3 = []  ## 空列表
    k = 0
    for i in range(len(list1)):
        tup1 = ()
        list2 = ["secretKey", "projectCode"]
        id = (list1[i]['secretKey'],)
        aaa = select_score_all(db_file1, id)
        # print(aaa)
        if aaa != []:
            k += 1
            continue
        else:
            for key in list2:
                if key in list1[i].keys():
                    tup2 = (list1[i][key],)
                else:
                    tup2 = ("",)
                tup1 = tup1 + tup2
        list3.append(tup1)
    print('数据库已存在数据%d条' % k)
    return list3


# 在已有数据中加入secretKey
def up_key(list3, db_file1):
    sql = '''
    UPDATE Project SET secretKey = ? WHERE projectCode = ?
    '''
    conn = get_db_conn(db_file1)
    cur = conn.cursor()  # 创建游标
    cur.executemany(sql, list3)  # 执行sql语句
    conn.commit()  # 提交结果
    close_db_conn(cur, conn)
    return cur.rowcount





if __name__ == "__main__":  # 当程序执行时
# 调用函数
    main1()
