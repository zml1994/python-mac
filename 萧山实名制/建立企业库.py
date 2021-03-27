import requests
from requests import HTTPError
import json
import time
import sqlite3
from sqlite封装 import get_db_conn, close_db_conn

db_file1 = 'xssmz.db'  # 数据库地址
i = 1  # 杭州的页码
n = 1  # 萧山的页码
j = 10  # 实名制数据每页大小
token = 'ae9c343c02af4e30a9a7771f4681a8d3'
# 添加杭州登录的cookie
headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-access-token': token}

# 添加萧山登录的cookie
headers1 = {"Cookie": ".ASPXAUTH=F84D986F05ABF15333E9B13536D1205602CECF45392435CFD1D45F3E2DA8F047EFDA9C2740352A5671C49C603F6F3FC9CBB266D3266BD5D9968884BC34CB80037219F90C3D2D10A20F5ABB0C5E2414432BC8576A733423550F6007594797FE5F"
           }

# 建表sql语句,如果表不存在，则创建；sql语句包含表名
sql1 = '''
            CREATE TABLE IF NOT EXISTS corp
            (id integer autoincrement,  -- 创建主键并自增长
        corpCode text UNIQUE,  -- 企业统一信用代码
        corpName text,  -- 企业名称
        hzis int,  -- 杭州是否存在
        xsis int,  -- 萧山是否存在
        PRIMARY KEY(id, corpCode) 
        );
        '''


# 定义用于请求杭州企业库的url
url = ' http://115.233.209.232:9000/api/company/findCompany/%d/%d' % (i, j)
# 定义用于请求萧山企业库的url
url1 = 'http://xs.pt.pinming.cn/Basic/Company/PageList??page=%d&rows=%d' % (n, j)

# 主函数，用于梳理流程程序逻辑
def main():
    # 0、建表
    init_db(db_file1, sql1)
    # 1、请求杭州企业库
    list = askUrlPost(url, headers)
    list1 = list[0]
    print(list1)
    print(list[1])
    # for i in range(2, len(list[1])+1):
    # 2、将数据写入数据库
    # 3、请求萧山企业库
    # 4、将数据写入企业库






    # # 1、建表，需要提供数据库路径，sql语句
    # init_db(db_file1, sql1)
    # # 2、发起请求，返回数据（列表）
    # print("2、正在发起请求数据")
    # r = askUrl(url, headers)
    # # 3、提取请求结果中的数据
    # list1 = tiqu1(r, "rows")
    # # 4、对请求的数据进行处理
    # print("4、处理数据，构建新增数据列表中。。。")
    # list3 = uplist(list1, db_file1)  # 构建批量插入数据的列表
    # print("5、添加新增项目到数据库中")
    # if list3 == []:
    #     print("  数据库新增数据0条")
    # else:
    #     row = insert_mult_data(list3, db_file1)  # 统计插入的函数
    #     print("  数据库新增数据%d条" % row)
    # # 更新施工许可证近100个项目
    # sigong()


# 创建数据表
def init_db(db_file, sql):
    conn = get_db_conn(db_file)
    cur = conn.cursor()  # 创建游标
    try:
        conn.execute(sql)
        print('1、建表成功/表已创建')
    except:
        print('1、建表失败')
        return False
    conn.commit()  # 提交结果
    close_db_conn(cur, conn)


# 请求 项目库，返回数据（列表）
def askUrlGet(url, headers):
    try:
        r = requests.get(url, headers=headers)
    except HTTPError as e:
        print(e.reason)
    r.encoding = 'utf-8'
    # print("3、请求结果原文如下\n%s" % r.text)

    # 打印请求结果，并省略原数据
    data = r.json()
    data['rows'] = '省略原数据'
    print("3、请求结果如下：\n%s" % data)
    return r.json()


def askUrlPost(url, headers):
    data = {"types": []}  # 空字典
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
    print("项目总数总数：%s\n" % r.json()['data']['total'])
    data = r.json()['data']
    list1 = [data['list'],r.json()['data']['totalPage']]
    return list1


# 提取返回结果中的数据
def tiqu1(r, key):
    list1 = r[key]
    print("  本次查询结果共%d条数据" % len(list1))
    return list1


# 构建批量插入数据的列表和更新密钥的列表
def uplist(list, db_file1):
    list3 = []  # 空列表
    k = 0
    j = 0
    m = 0
    for i in range(len(list)):
        tup1 = ()
        tup3 = ()
        list2 = ['ProjectID', 'ProName', 'ProjectCategory', 'ProStatus', 'ConsUnitName', 'ShigongUnitName', 'ProjectCode', 'SecretKey']  # 设定所需要的字段
        ProjectID = (list[i]['ProjectID'],)
        # 查找id是否在数据库存在，返回（萧山实名制平台未对接）标记，0为等待更新密钥
        aaa = select_score_all(db_file1, ProjectID)

        # 如果返回结果为[],则需要新增数据
        if aaa != []:
            # 如果返回结果（萧山实名制平台未对接）标记为0（0为等待更新密钥），且该项目有新密钥，则更新xsappid及密钥
            if aaa[0][0] == 0 and list[i]['ProjectCode'] != '':
                sql3 = '''
                    UPDATE Project SET xsProjectCode = ?, xsSecretKey = ?,xsProjectCodeis= 1 WHERE ProjectID = ?
                    '''
                tup3 = [(list[i]['ProjectCode'], list[i]['SecretKey'], list[i]['ProjectID'])]
                up_key(tup3, db_file1, sql3)
                j += 1
            k += 1  # 统计存在次数
            continue
        # 如果返回结果为空[]，代表该项目不在数据库中，需要新增。
        else:
            # 根据list2，构建需要批量添加的列表数据
            for key in list2:  # 构建批量插入所需要的元组
                if key in list[i].keys():  # 如果数据中不存在该字段，用空元祖替代
                    tup2 = (list[i][key],)
                else:
                    tup2 = ("",)
                tup1 = tup1 + tup2
            # 如果第7个值为空，代表无xsappid，标记为0
            if tup1[6] == '':
                is1 = 0
            # 如果第7个值为数值，代表有xsappid，标记为1
            else:
                is1 = 1
            # 添加一个默认标记及创建数据的时间
            time1 = (is1, 0, time.strftime("%Y-%m-%d", time.localtime()),)
        # 将元组逐个添加到列表中
        list3.append(tup1 + time1)
    print('  数据库已存在数据%d条，萧山更新对接项目%d个' % (k, j))
    return list3


# 查询数据
def select_score_all(db_file, id):
    sql = '''select xsProjectCodeis from Project where ProjectID =?
    '''
    conn = sqlite3.connect(db_file)  # 打开或创建数据库文件
    cur = conn.cursor()  # 创建游标
    cur.execute(sql, id)  # 执行sql语句
    # print(cur.fetchall())  # 打印所有结果
    aaa = cur.fetchall()
    cur.close()  # 关闭游标
    conn.close()  # 关闭数据库
    return aaa


# 批量插入数据
def insert_mult_data(list3, db_file1):
    sql = '''insert into Project (
        ProjectID,
        ProName,
        ProjectCategory,
        ProStatus,
        ConsUnitName,
        ShigongUnitName,
        xsProjectCode,
        xsSecretKey,
        xsProjectCodeis,
        hzProjectCodeis,
        time)
        values(?,?,?,?,?,?,?,?,?,?,?)   -- 元组
        '''
    conn = get_db_conn(db_file1)  # 连接数据库
    cur = conn.cursor()  # 创建游标
    cur.executemany(sql, list3)  # 执行sql语句
    conn.commit()  # 提交结果
    close_db_conn(cur, conn)  # 关闭游标及连接
    return cur.rowcount


# 将有appid、密钥的项目，数据更新到数据库中，并更新标记
def up_key(list3, db_file1, sql):
    conn = get_db_conn(db_file1)
    cur = conn.cursor()  # 创建游标
    cur.executemany(sql, list3)  # 执行sql语句
    conn.commit()  # 提交结果
    close_db_conn(cur, conn)
    return cur.rowcount


# 更新施工许可证数据
def sigong():
    r = askUrl(url1, headers)
    list1 = tiqu1(r, "rows")
    for i in range(len(list1)):
        # tup1 = ()
        # tup3 = ()
        # list2 = ['ProjectID', 'ProName', 'ProjectCategory', 'ProStatus', 'ConsUnitName', 'ShigongUnitName', 'ProjectCode', 'SecretKey']  # 设定所需要的字段
        ProjectID = list1[i]['ProjectID']
        ConsNo = list1[i]['ConstructionPermitNo']
        list = [(ConsNo, ProjectID)]
        # print(list)
        sql4 = '''
            UPDATE Project SET ConsNo = ? WHERE ProjectID = ?
            '''
        up_key(list, db_file1, sql4)


if __name__ == "__main__":  # 当程序执行时
    main()