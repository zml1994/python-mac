import requests
from requests import HTTPError
import json
import time
import sqlite3
from sqlite封装 import get_db_conn, close_db_conn

db_file1 = 'xssmz.db'  # 数据库地址
n = 1  # 页码
j = 10  # 实名制数据每页大小
l = 100  # 施工许可证每页大小

# 添加cookie用于登录
headers = {"Cookie": ".ASPXAUTH=F84D986F05ABF15333E9B13536D1205602CECF45392435CFD1D45F3E2DA8F047EFDA9C2740352A5671C49C603F6F3FC9CBB266D3266BD5D9968884BC34CB80037219F90C3D2D10A20F5ABB0C5E2414432BC8576A733423550F6007594797FE5F"
           }

# 建表sql语句,如果表不存在，则创建；sql语句包含表名
sql1 = '''
            CREATE TABLE IF NOT EXISTS Project
            (id integer primary key autoincrement,  -- 创建主键并自增长
        ProjectID text,  -- 萧山项目id
        ProName text,  -- 萧山项目名称
        ConsNo text,  -- 施工许可证 
        lsConsNo text, -- 临时施工许可证
        ProjectCategory text,  -- 项目类别
        ProStatus text,  -- 项目状态
        ConsUnitName text,  -- 建设单位
        ConsUnitNameCode text,  -- 建设单位统一社会信用代码
        ShigongUnitName text,  -- 施工单位
        ShigongUnitNameCode text,  -- 施工单位统一社会信用代码
        xsProjectCode text,  -- 萧山实名制id
        xsProjectCodeis int,  -- 判断萧山项目及密钥是否生成(0表示未创建，1表示已创建）
        xsSecretKey text,  -- 萧山实名制对接密钥
        hzProjectCode text,  -- 杭州实名制id
        hzProjectCodeis int,  -- 判断杭州项目是否创建(0表示未创建，1表示已创建）
        hzSecretKey text,  -- 杭州实名制对接密钥
        hzSecretKeyis int,  -- 判断杭州项目是否报备（密钥是否生成）(0表示未创建，1表示已创建）
        time text  -- 数据添加日期
        );
        '''

# 定义用于请求萧山实名制的url
url = 'http://xs.pt.pinming.cn/RealName/RealProject/PageList?page=%d&rows=%d' % (n, j)
# 用于请求萧山施工许可证的url
url1 = 'http://xs.pt.pinming.cn/Supervision/ConstructionPermit/PageList?page=%d&rows=%d' % (n, l)

# 主函数，用于梳理流程程序逻辑
def main():
    # 1、建表，需要提供数据库路径，sql语句
    init_db(db_file1, sql1)
    # 2、发起请求，返回数据（列表）
    print("2、正在发起请求数据")
    r = askUrl(url, headers)
    # 3、提取请求结果中的数据
    list1 = tiqu1(r, "rows")
    # 4、对请求的数据进行处理
    print("4、处理数据，构建新增数据列表中。。。")
    list3 = uplist(list1, db_file1)  # 构建批量插入数据的列表
    print("5、添加新增项目到数据库中")
    if list3 == []:
        print("  数据库新增数据0条")
    else:
        row = insert_mult_data(list3, db_file1)  # 统计插入的函数
        print("  数据库新增数据%d条" % row)
    # 更新施工许可证近100个项目
    sigong()
    tongji()


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
def askUrl(url, headers):
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

# 统计数据库情况
def tongji():
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


if __name__ == "__main__":  # 当程序执行时
    main()
