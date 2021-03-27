import requests
from requests import HTTPError
import json
import time
import sqlite3
from sqlite封装 import get_db_conn, close_db_conn
from CorpQuery import CorpQuery


db_file1 = 'xssmz.db'  # 数据库地址
n = 1  # 页码
j = 2000  # 每页大小

# 遍历数据库标记为0的项目
# 1、获取施工许可证或创建施工许可证
# 2、从杭州平台查询企业是否存在
# 3、如存在，则记录到数据库，如不存在，则企查查查询
# 4、从企查查查询统一社会信用代码
# 5、如查询到，则记录到数据库，在查询该企业是否在杭州平台
# 6、如该企业不在杭州平台，则推送至杭州平台
# 7、如查询不到，则手工处理。
# 8、将数据写入到excel中
# 9、导入企业
# 10、根据查询，查询appid并写入数据库，改标记为1



def main():
    corpCode = ''
    corpName = '上辰工程管理(浙江)有限公司'
    data = CorpQuery(corpCode, corpName)
    # print(data)
    if data['data']['totalCount'] != 0:
        print(data['data']['rows'][0]['corpCode'])
        print("查询不到该企业")
    else:
        print("杭州市平台查询不到该企业")
    return






# 请求方式：GET
# 请求URL：https://api.qianzhan.com/OpenPlatformService/GetToken
# 请求参数：
# type=JSON&appkey=cd4461e04c6c1660&seckey=e6ebe170c151e923
#
#
# 请求方式：GET
# 请求URL：https://api.qianzhan.com/OpenPlatformService/OrgCompanyListByCompanyName
# 请求参数：
# token=d8abd71926a1849fe3ae8717e35ba231&type=JSON&companyName=%E6%9D%AD%E5%B7%9E%E5%93%81%E8%8C%97%E5%AE%89%E6%8E%A7%E4%BF%A1%E6%81%AF%E6%8A%80%E6%9C%AF%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8



# 请求 项目库，返回数据（列表）
def askUrl(url, headers):
    try:
        r = requests.get(url, headers=headers)
    except HTTPError as e:
        print(e.reason)
    r.encoding = 'utf-8'
    print("3、请求结果原文如下\n%s" % r.text)

    # 打印请求结果，并省略原数据
    data = r.json()['rows']
    print(len(data))
    # data['rows'] = '省略原数据'
    # print("3、请求结果如下：\n%s" % data)
    return r.json()

if __name__ == "__main__":  # 当程序执行时
    main()