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
TableName_hzbb = '`hz(xs)-ybb-project`'
# TableName_hzbb = '`test3`'
TableName_xsconfigList = '`tsconfiglist-xs-to-hz`'

# 请求基础配置
token = '1f856617f2064342a42b0c18e6109e4d'
headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'x-access-token': token}
pageNo_s = 1  # 起始页
pageSize = 100

def get_token1():
    print('正在获取token！！')
    url = f'http://47.110.228.86:8081/api/login'
    data = {'username': 'superadmin',
            'password': 'Aa123456'}
    try:
        r = requests.post(url, data=data)
    except HTTPError as e:
        print(f'        请求出错,原因是{e.reason}')
    r.encoding = 'utf-8'
    results = r.json()['message']
    # results = r.json()
    print(f'            添加结果为：{results}')
    return r.json()['data']['authValue']

token1 = get_token1()
headers1 = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'x-access-token': token1}

# 请求url参数配置
projectStatus = ''  # 项目状态
isRegister = '0'  # 是否报备  0：所有  1：未报备
govOrgIds = [14]  # 监管机构，14：萧山区


# 自动配置萧山已报备项目
def main():


    # results_tuple = caxun()
    # chanshi_addConfig(results_tuple)
    xstohzzdpz()

def xstohzzdpz():
    # 查询萧山已报备项目并写入数据库
    xsbb()
    # 查询萧山推送已配置项目并写入数据库
    xspz()
    # 查询两个数据库，获取未对接项目
    results_tuple = caxun()
    # 根据项目名称，尝试配置密钥
    chanshi_addConfig(results_tuple)


# 根据数据库查询结果，尝试配置
def chanshi_addConfig(results_tuple):
    print(f'4、共有{len(results_tuple)}个项目已报备但未对接!!')
    print(f'根据项目名称，尝试配置！\n')
    for i in results_tuple:
        projectName = i[0]
        appId = i[1]
        secretKey = i[2]
        print(f'    该项目的添加时间为：{i[3]}，正在尝试配置项目{projectName}')
        addConfig(projectName, appId, secretKey)


# 查询萧山配置，并写入数据
def xspz():
    print('1、正在发起循环请求数据')
    list_all = askUrl_configList()
    print(f'2、请求完毕！总共{len(list_all)}条数据，正在写入数据到数据库')

    # 写入数据
    r = InsertData(TableName_xsconfigList, list_all)

    print(f'3、数据写入完毕！\n')


def xsbb():
    # 请求所有数据
    print('1、正在发起循环请求数据')
    list_all = xunhuan(pageNo_s)
    # print(list_all)
    # 对所有数据，进行循环写入
    print(f'2、请求完毕！总共{len(list_all)}条数据，正在写入数据到数据库')
    r = InsertData(TableName_hzbb, list_all)
    print(f'3、数据写入完毕！\n')


# 请求萧山推送杭州的配置列表
def askUrl_configList():
    url = 'http://47.110.228.86:8081/api/push/config/1/10000/configList?platformName=%E6%9D%AD%E5%B7%9E%E5%B9%B3%E5%8F%B0'
    try:
        r = requests.get(url, headers=headers1)
    except HTTPError as e:
        print(e.reason)
    r.encoding = 'utf-8'
    # print("3、请求结果原文如下\n%s" % r.text)

    # 打印请求结果，并省略原数据
    data = r.json()
    data['data']['list'] = '省略原数据'
    print(f'3、请求结果如下：\n{data}')
    return r.json()['data']['list']


# 添加项目推送配置（萧山至杭州）
def addConfig(projectName, appId, secretKey):
    url = f'http://47.110.228.86:8081/api/push/config/addConfig'
    data = {
        'platformName': '杭州f平台',
        'platformKey': 'hangzhou',
        'pushUrl': 'http://115.233.209.232:9089/open.api',
        'pushAppId': appId,
        'pushProjectCode': appId,
        'pushSecurityKey': secretKey,
        'myProjectName': projectName,
        'myProjectCode': ''
    }
    # print(data)
    # print(headers1)
    try:
        r = requests.post(url, data=data, headers=headers1)
    except HTTPError as e:
        print(f'        请求出错,原因是{e.reason}')
    r.encoding = 'utf-8'
    results = r.json()['message']
    results = r.json()
    print(f'            添加结果为：{results}')



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
            time.sleep(random.randint(0, 10) * 0.1)
    return list_all


# 查询未对接项目
def caxun():
    db = pymysql.connect(host=host, port=port, user=user, passwd=pw, db=db_name)
    cur = db.cursor()
    n = cur.execute(
        f'Select `projectName`, `appId`, `secretKey`, `addtime` FROM {TableName_hzbb} where appid not in (Select pushAppid FROM {TableName_xsconfigList})')
    # print(f'Select `projectName`, `appId`, `secretKey`, `addtime` FROM {TableName_hzbb} where appid not in (Select pushAppid FROM {TableName_xsconfigList})')
    results = cur.fetchall()
    db.commit()
    cur.close()
    db.close()
    # print(results)
    # print(len(results))
    return results


# 自定义列表，写入mysql
def InsertData(TableName, list_all):
    # 将当前时间添加到需要写入的字典中
    # print(TableName)
    if TableName == '`hz(xs)-ybb-project`':
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
    elif TableName == '`tsconfiglist-xs-to-hz`':
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
            # print(kk)
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


if __name__ == "__main__":  # 当程序执行时
    print('Start：开始执行程序\n')
    time_start = time.time()
    main()
    t = time.time() - time_start
    print(f'\nEnd：程序执行完毕！总共执行时间：{int(t / 60)}分 {int(t % 60)}秒!')
