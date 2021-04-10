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
TableName_hzbb = '`hz-xs-ybb-project`'
TableName_xsconfigList = '`hz-xs-configList`'

# 请求基础配置
token = 'b9deb2a9df4147db8f0f6b50ef037c1b'
headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'x-access-token': token}
pageNo_s = 1  # 起始页
pageSize = 100

# 请求url参数配置
projectStatus = '003'  # 项目状态
isRegister = '0'  # 是否报备
govOrgIds = [14]  # 监管机构，14：萧山区


def main():
    xsbb()
    xspz()


def xspz():
    print('1、正在发起循环请求数据')
    list_all = askUrl_configList()
    print(f'2、请求完毕！总共{len(list_all)}条数据，正在写入数据到数据库')

    # 写入数据
    r = InsertData(TableName_xsconfigList, list_all)

    print(f'3、数据写入完毕！')

def xsbb():
    # 请求所有数据
    print('1、正在发起循环请求数据')
    list_all = xunhuan(pageNo_s)
    # 对所有数据，进行循环写入
    print(f'2、请求完毕！总共{len(list_all)}条数据，正在写入数据到数据库')
    r = InsertData(TableName_hzbb, list_all)
    print(f'3、数据写入完毕！\n')



def askUrl_configList():
    url = 'http://47.110.228.86:8081/api/push/config/1/10000/configList?platformName=%E6%9D%AD%E5%B7%9E%E5%B9%B3%E5%8F%B0'
    try:
        r = requests.get(url, headers=headers)
    except HTTPError as e:
        print(e.reason)
    r.encoding = 'utf-8'
    # print("3、请求结果原文如下\n%s" % r.text)

    # 打印请求结果，并省略原数据
    data = r.json()
    data['data']['list'] = '省略原数据'
    print(f'3、请求结果如下：\n{data}')
    return r.json()['data']['list']

# 请求url 杭州市项目库，返回数据（列表）
def askUrl(pageNo, pageSize, projectStatus, isRegister, govOrgIds):
    global r
    url = f'http://115.233.209.232:9000/api/realname/project/register/{pageNo}/{pageSize}/findProjectRegister'
    data = {
        'projectStatus': projectStatus,
        'isRegister': isRegister,
        'projectName': '',
        'govOrgIds': govOrgIds
    }
    # 请求异常判断
    try:
        r = requests.post(url, json=data, headers=headers)
    except HTTPError as e:
        print(f'    请求出错,原因是{e.reason}')
    r.encoding = 'utf-8'
    # print(r.text)  # 打印原始请求数据
    # 如果请求结果为401，返回401
    if r.json()['code'] == 401:
        return r.json()['code'], 0
    # 如果请求结果正常，返回list
    else:
        list1 = r.json()['data']['list']
        total = r.json()['data']['total']
        totalPage = r.json()['data']['totalPage']
        print(f'    分页请求: 每页{pageSize}条，请求{pageNo}页')
        print(f'    返回结果:共{total}条数据，共{totalPage}页\n')
        return list1, totalPage

# 循环请求，返回list_all
def xunhuan(pageNo_s, totalPage=100000):  # 定义totalPage初始变量，足够大就行
    list_all = []  # 定义空列表，用于接受查询数据并返回

    # 根据起始页，进行循环请求
    while pageNo_s <= totalPage:
        # 发起请求，返回list数据及总共多少页
        list1, totalPage = askUrl(pageNo_s, pageSize, projectStatus, isRegister, govOrgIds)
        # 如果返回结果是401，则停止
        if list1 == 401:
            print('token失效，请更新token！！')
        # 返回结果正常，对list进行叠加
        else:
            list_all += list1
            pageNo_s += 1
            time.sleep(random.randint(0, 10)*0.1)
    return list_all


# 自定义列表，写入mysql
def InsertData(TableName, list_all):
    # 将当前时间添加到需要写入的字典中
    if TableName == '`hz-xs-ybb-project`':
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
        kk = 'projectId'
    elif TableName == '`hz-xs-configList`' or TableName == '`test2`' :
        list = [
            'myProjectCode',
            'projectName',
            'pushAppId',
            'pushProjectCode',
            'pushSecurityKey',
            'pushUrl',
            'createTime',
            'addtime'
        ]
        kk = 'pushProjectCode'
    # 对pymysql进行异常判断
    try:
        db = pymysql.connect(host=host, port=port, user=user, passwd=pw, db=db_name)
        cur = db.cursor()
        t = 0
        f = 0
        for dic in list_all:
            dic['addtime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 根据projectId查找数据库是否存在！
            keyword = dic[kk]
        # print(f'select {kk} from {TableName} where {kk} = {keyword}')
            n = cur.execute(f'select {kk} from {TableName} where {kk} = \'{keyword}\'')
        # 数据库不存在，构建写入数据库的列名称、行内容字段
            if n == 0:
                COLstr = ''  # 列的字段
                ROWstr = ''  # 行字段
                # 根据自定义字段，循环构建列名称、行内容字段
                for key in list:
                    COLstr = COLstr + key + ','
                    # 如果key在字典中存在，写入value；不存在，写入”无“
                    if key in dic:
                        val = f'"{dic[key]}"'
                    else:
                        val = '"无"'
                    ROWstr = ROWstr + val + ','
                # 执行sql，写入数据
                cur.execute(f'INSERT INTO {TableName}({COLstr[:-1]}) VALUES ({ROWstr[:-1]})')
                t += 1
                # print(f't={t}')
            else:
                f += 1
                # print(f'f={f}')
        print(f'新增{t}条数据，{f}条数据已存在！')
        db.commit()
        cur.close()
        db.close()
    except pymysql.Error as e:
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
        print(f'执行的sql语句： INSERT INTO {TableName}({COLstr[:-1]}) VALUES ({ROWstr[:-1]})')


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
    print(f'\nEnd：程序执行完毕！总共执行时间：{int(t / 60)}分 {int(t % 60)}秒!')