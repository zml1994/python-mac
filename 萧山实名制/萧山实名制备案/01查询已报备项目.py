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
TableName = 'hz-xs-ybb-project'

# 请求相关信息
token = '3ac5d38937234362ad09cb650beddb4e'
headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-access-token': token}
pageNo =1
pageSize = 100

dict = {
        "address": "南阳街道左十四线与南庄路交叉口向西50米",
        "appId": "330109210329010002",
        "buildCorpCode": "11330109002514224B",
        "buildCorpNames": "杭州市公安局萧山区分局",
        "builderLicenseNumber": "330109202101080201",
        "buildingArea": 9460.00,
        "category": "01",
        "categoryName": "房屋建筑工程",
        "city": "杭州市",
        "contractorCorpCode": "913301096917328679",
        "contractorCorpNames": "港立建设（浙江）有限公司",
        "county": "萧山区",
        "dockCountryPlatform": False,
        "govOrgNames": "杭州钦汇建设工程管理有限公司淳安分公司",
        "invest": 2972.6398,
        "orgName": "萧山区",
        "projectArea": "浙江省杭州市萧山区南阳街道",
        "projectCode": "330109210329010002",
        "projectId": 8481,
        "projectName": "南阳派出所新建工程项目",
        "projectStatus": "003",
        "projectStatusName": "在建",
        "province": "浙江省",
        "registerId": "5434",
        "secretKey": "?igIAb@$R7+h@48Ymyn29r3r8/#DV-lX",
        "street": "南阳街道",
        "workerCount": 0
      }

def main():
    # xunhuan()

    InsertData(TableName,dict)


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

    # 输出结果
    list1 = r.json()['data']['list']
    total = r.json()['data']['total']
    totalPage = r.json()['data']['totalPage']
    print(f'请求结果如下，现请求{pageNo}页，每页{pageSize}条，共{total}条数据，共{totalPage}页')
    return list1, totalPage

def xunhuan():
    list_all = []
    totalPage = 100000
    pageNo = 1
    while pageNo <= totalPage:
        list1, totalPage = askUrl(pageNo, pageSize)
        list_all += list1
        pageNo += 1
        time.sleep(random.randint(0, 2))
    print(f'请求完毕,总共有{len(list_all)}条数据')
    return list_all


    # # 打印请求结果，并省略原数据
    # data = r.json()
    # data['rows'] = '省略原数据'
    # print("3、请求结果如下：\n%s" % data)
    # return r.json()


def InsertData(TableName, dic):
    try:
        db = pymysql.connect(host=host, port=port, user=user, passwd=pw, db=db_name)
        cur = db.cursor()
        COLstr = ''  # 列的字段
        ROWstr = ''  # 行字段

        ColumnStyle = 'CHAR(40)'
        for key in dic.keys():
            COLstr = COLstr + ' ' + key + ColumnStyle + ','
            print(COLstr)
            ROWstr = (ROWstr + '"%s"' + ',') % (dic[key])
            print(ROWstr)

        # 推断表是否存在，存在运行try。不存在运行except新建表，再insert
        try:
            cur.execute("SELECT * FROM %s" % TableName)
            cur.execute("INSERT INTO %s VALUES (%s)" % (TableName, ROWstr[:-1]))

        except pymysql.Error as e:
            cur.execute("CREATE TABLE %s (%s)" % (TableName, COLstr[:-1]))
            cur.execute("INSERT INTO %s VALUES (%s)" % (TableName, ROWstr[:-1]))
        db.commit()
        cur.close()
        db.close()

    except pymysql.Error as e:
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))


    # db = pymysql.connect(host=host, port=port, user=user, passwd=pw, db=db_name)
# cursor = db.cursor()
# cursor.execute("SELECT VERSION()")
# data = cursor.fetchone()
# print('Database version : %s' % data)
# db.close()



if __name__ == "__main__":  # 当程序执行时
    print('Start：开始执行程序\n')
    time_start = time.time()
    main()
    t = time.time() - time_start
    print(f'End：程序执行完毕，总共执行时间：{int(t / 60)}分 {int(t % 60)}秒!')
