import requests
from requests import HTTPError
import json
import time
import sqlite3
from sqlite封装 import get_db_conn, close_db_conn
from 项目报备 import main1
db_file1 = 'hzsmz.db'
m = 1
n = 66  # 页码
j = 100  # 每页大小
token = '9f125e31c42345c78c9d909daba8c1a4'


def main():
    init_db(db_file1)
    for i in range(m, n):
        list1 = askUrl(i, j)
        # print(list1)
        list3 = uplist(list1, db_file1)
        if not list3:
            print("数据库新增数据0条")
        else:
            row = insert_mult_data(list3, db_file1)
            print("数据库新增数据%d条\n" % row)
        # print("开始执行项目报备数据")
    # main1(token)


# 请求 项目库
def askUrl(i, j):
    url = 'http://115.233.209.232:9000/api/project/findProject/%d/%d' % (i, j)
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-access-token': token}
    data = {}  # 空字典
    # data = json.dumps(data)   #  序列化成json
    r = requests.post(url=url, json=data, headers=headers)
    r.encoding = 'utf-8'
    # print(r.json())
    # print("post执行状态码：%s" % r.json()['code'])
    print("页码：%s" % r.json()['data']['pageNum'])
    # print("每页大小：%s" % r.json()['data']['pageSize'])
    # print("总共%s页" % r.json()['data']['totalPage'])
    # print("项目总数总数：%s\n" % r.json()['data']['total'])
    data = r.json()['data']
    list1 = data['list']
    return list1


# 查询数据
def select_score_all(db_file, id):
    sql = '''select * from Project5 where projectCode =?
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
        list2 = ["address", "areaId", "builderLicenseNumber", "buildingArea", "category", "categoryName", "city",
                 "completeDate", "contractorCorpNames", "county", "govOrgId", "invest", "lat", "lng", "orgName",
                 "projectArea", "projectCode", "projectId", "projectName", "projectStatus", "projectStatusName",
                 "province",
                 "small", "startDate", "street"]
        id = (list1[i]['projectCode'],)
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
    sql = '''insert into Project5 (
        address,
        areaId,
        builderLicenseNumber,
        buildingArea,
        category,
        categoryName,
        city,
        completeDate,
        contractorCorpNames,
        county,
        govOrgId,
        invest,
        lat,
        lng,
        orgName,
        projectArea,
        projectCode,
        projectId,
        projectName,
        projectStatus,
        projectStatusName,
        province,
        small,
        startDate,
        street,
        time)
        values(
        ?,?,?,?,?,?,?,?,
        ?,?,?,?,?,?,?,?,?,
        ?,?,?,?,?,?,?,?,?
        )   -- 元组
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
            CREATE TABLE IF NOT EXISTS Project5
            (id integer primary key autoincrement,
        address text,
        areaId int,
        builderLicenseNumber text,
        buildingArea text,
        category text,
        categoryName text,
        city text,
        completeDate text,
        contractorCorpNames text,
        county text,
        govOrgId int,
        invest REAL,
        lat REAL,
        lng REAL,
        orgName text,
        projectArea text,
        projectCode text,
        projectId int,
        projectName text,
        projectStatus text,
        projectStatusName text,
        province text,
        small int,
        startDate text,
        street text,
        secretKey text,
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
# init_db("movie.db")
