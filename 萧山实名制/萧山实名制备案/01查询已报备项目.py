from datetime import datetime
import requests
from requests import HTTPError
import json
import time
import pymysql
import random
# 数据库配置信息
host = 'rm-bp1ya4u34kwfscg7ido.mysql.rds.aliyuncs.com'
port = 3306
user = 'zml'
pw = 'Aa123456'
db_name = 'xssmz'
TableName = '`hz-xs-ybb-project`'

# 请求相关信息
token = '8643d34830384e10a7a6d633c41eaf36'
headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-access-token': token}
pageNo =1
pageSize = 100


def main():
    # 请求所有数据
    list_all = xunhuan()
    # 对所有数据，进行循环写入
    for i in range(len(list_all)):
        # print(list_all[i])
        print(f'正在写入第{i+1}条数据,总共{len(list_all)}条 ', end='')

        # 写入数据
        InsertData(TableName, list_all[i])


# 请求 项目库，返回数据（列表）
def askUrl(pageNo, pageSize):
    print(f'正在请求杭州市项目库，第{pageNo}页，{pageSize}条/页')
    url = f'http://115.233.209.232:9000/api/realname/project/register/{pageNo}/{pageSize}/findProjectRegister'
    data = {
        'projectStatus': '003',  # 项目状态
        'isRegister': '0',  # 是否报备
        'projectName': '',  # 项目名称
        'govOrgIds': [14]  # 监管机构，14：萧山区
    }

    # 请求异常判断
    try:
        r = requests.post(url, json=data, headers=headers)
    except HTTPError as e:
        print(f'    请求出错,原因是{e.reason}')
    r.encoding = 'utf-8'
    # print(r.text)  # 打印原始请求数据
    if r.json()['code'] == 401:
        print('token失效，请更新token！！')
        return r.json()['code'], 0
    else:
        list1 = r.json()['data']['list']
        total = r.json()['data']['total']
        totalPage = r.json()['data']['totalPage']
        print(f'请求结果如下，现请求{pageNo}页，每页{pageSize}条，共{total}条数据，共{totalPage}页')
        return list1, totalPage

def xunhuan():
    list_all = []
    totalPage = 100000
    pageNo = 1
    # 根据第一次请求，更新totalpage。
    while pageNo <= totalPage:
        list1, totalPage = askUrl(pageNo, pageSize)
        if list1 == 401:
            break
        else:
            list_all += list1
            pageNo += 1
            # totalPage = 1
            time.sleep(random.randint(0, 2))
    print(f'请求完毕,总共有{len(list_all)}条数据')
    return list_all

# 自定义列表，写入mysql
def InsertData(TableName, dic):
    dic['addtime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        db = pymysql.connect(host=host, port=port, user=user, passwd=pw, db=db_name)
        cur = db.cursor()
        # print(f'select projectId from {TableName} where projectId = {dic["projectId"]}')
        n = cur.execute(f'select projectId from {TableName} where projectId = {dic["projectId"]}')

        if n == 0:
            COLstr = '' # 列的字段
            ROWstr = '' # 行字段
            list = [
                    'appId',
                    'projectId',
                    'buildCorpCode',
                    'buildCorpNames',
                    'contractorCorpCode',
                    'contractorCorpNames',
                    'govOrgNames',
                    'builderLicenseNumber',
                    'orgName',
                    'projectName',
                    'projectStatus',
                    'projectStatusName',
                    'secretKey',
                    'workerCount',
                    'addtime'
                    ]
            # print(dic)
            ColumnStyle = ' CHAR(40)'
            for key in list:
                COLstr = COLstr + key +','
                if key in dic:
                    val = f'"{dic[key]}"'
                else:
                    val = '"无"'
                ROWstr = ROWstr + val + ','
            # COLstr = COLstr + 'addtime' + ','
            # ROWstr = ROWstr + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ','
            cur.execute("SELECT * FROM %s" % TableName)
            cur.execute(f'INSERT INTO {TableName}({COLstr[:-1]}) VALUES ({ROWstr[:-1]})')
            print('写入成功！')
        else:
            print('已存在！')

        db.commit()
        cur.close()
        db.close()
    except pymysql.Error as e:
        print(f'  INSERT INTO {TableName}({COLstr[:-1]}) VALUES ({ROWstr[:-1]})')
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))




# 无效  字典写入到mysql
def InsertData1(TableName, dic):
    try:
        db = pymysql.connect(host=host, port=port, user=user, passwd=pw, db=db_name)
        cur = db.cursor()
        COLstr = ''  # 列的字段
        ROWstr = ''  # 行字段

        ColumnStyle = ' CHAR(40)'
        for key in dic.keys():
            COLstr = COLstr + ' ' + key + ColumnStyle + ','
            ROWstr = (ROWstr + f'"{dic[key]}"' + ',')

        # 推断表是否存在，存在运行try。不存在运行except新建表，再insert
        try:
            cur.execute("SELECT * FROM %s" % TableName)
            cur.execute(f'INSERT INTO {TableName}({COLstr[:-1]}) VALUES ({ROWstr[:-1]})')

        except pymysql.Error as e:
            cur.execute("CREATE TABLE %s (%s)" % (TableName, COLstr[:-1]))
            cur.execute("INSERT INTO %s VALUES (%s)" % (TableName, ROWstr[:-1]))
        db.commit()
        cur.close()
        db.close()
    except pymysql.Error as e:
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))


if __name__ == "__main__":  # 当程序执行时
    print('Start：开始执行程序\n')
    time_start = time.time()
    main()
    t = time.time() - time_start
    print(f'End：程序执行完毕，总共执行时间：{int(t / 60)}分 {int(t % 60)}秒!')
