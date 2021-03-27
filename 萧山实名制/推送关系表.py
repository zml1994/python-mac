import requests
import json
import time
import sqlite3
from sqlite封装 import get_db_conn, close_db_conn

db_file1 = 'xssmz.db'
# n = 1  # 页码
# j = 1000  # 每页大小

def main():
    init_db(db_file1)  # 建表
    list1 = askUrl()  # 请求数据
    print(list1)
    list3 = uplist(list1, db_file1)  # 构建批量插入数据的列表
    if list3 == []:
        print("数据库新增数据0条")
    else:
        row = insert_mult_data(list3, db_file1)
        print("数据库新增数据%d条" % row)


# 请求 项目库
def askUrl():
    url = 'http://47.110.228.86:8081/api/push/config/1/10000/configList?'
    r = requests.get(url)
    r.encoding = 'utf-8'
    list1 = r.json()['data']['list']
    return list1


# 查询数据
def select_score_all(db_file, id):
    sql = '''select * from XSts where myProjectCode =?
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
        list2 = ['createTime', 'myProjectCode', 'projectId', 'projectName', 'pushAppId', 'pushSecurityKey']
        id = (list1[i]['myProjectCode'],)
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
            time1 = (time.strftime("%Y-%m-%d", time.localtime()),)
        list3.append(tup1 + time1)
    print('数据库已存在数据%d条' % k)
    return list3


# 批量插入数据
def insert_mult_data(list3, db_file1):

        # list[i] = tuple(list[i])  # value
        # print((list[i]))
    sql = '''insert into XSts(
        createTime,
        myProjectCode,
        projectId,
        projectName,
        pushAppId,
        pushSecurityKey,
        time)
        values(?,?,?,?,?,?,?)   -- 元组
        '''
    # 构建一个元组
    conn = get_db_conn(db_file1)
    cur = conn.cursor()  # 创建游标
    cur.executemany(sql, list3)  # 执行sql语句
    conn.commit()  # 提交结果
    close_db_conn(cur, conn)
    return cur.rowcount


# 创建数据表
def init_db(db_file1):
    conn = get_db_conn(db_file1)
    cur = conn.cursor()  # 创建游标
    try:
        sql1 = '''
            CREATE TABLE IF NOT EXISTS XSts 
            (id integer primary key autoincrement,
        createTime text,
        myProjectCode text,
        projectId text,
        projectName text,
        pushAppId text,
        pushSecurityKey text,
        time text);
        '''
        conn.execute(sql1)
    except:
        print("建表失败")
        return False
    conn.commit()  # 提交结果
    close_db_conn(cur, conn)


if __name__ == "__main__":  # 当程序执行时
# 调用函数
    main()
