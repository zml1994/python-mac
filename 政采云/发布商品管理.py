# -*- coding: utf-8 -*-
import openpyxl
import requests
import json
import time
import random
m = 1  # 起始页码
n = 31  # 终止页
j = 100  # 每页大小
# cookies = dict(SESSION='ZDM5NTEwN2EtZGJlMS00MTJjLTk1OWQtOTA2ZGE5NWY0OWJm')
cookies = {'SESSION': 'MzhmNDg5OTktMDFmZC00Y2VlLTlmMWQtZjZiZjk4NGQyOTlm'}
headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
key1 = 'channel'  # 基础商品：'channel'    协议商品：'protocol'
key3 = 'UNDER_SHELF'  # 下架功能：'UNDER_SHELF'  删除功能：'DELETE'

# 实例化session
# session = requests.session()


# 定义主函数
def main():

    # # 打开json数据
    # with open('protocol下架.json', 'r', encoding='utf-8') as f:
    #     json_data = json.load(f)
    #     # print(type(json_data))
    #     l = len(json_data)
    #     # l = 20
    # with open('已销售商品id', 'r') as f:
    #     list1 = f.read().split('\n')
    #     # print(list1)
    # # 循环数据
    # d = 0
    # nd = 0
    # for i in range(l):
    #     # print(type(json_data[i]['discountRate']))
    #     # 根据优惠率来判断是否删除
    #     # if json_data[i]['discountRate'] > 50 or json_data[i]['discountRate'] < 5:
    #     #     print('优惠率为：%d，执行删除' % json_data[i]['discountRate'])
    #     #     itemId = json_data[i]['itemId']
    #     #     faqi(itemId, key4)
    #     #     d += 1
    #     # else:
    #     #     nd += 1
    #
    #     # 根据是否销售的list，id来判断是否删除
    #     itemId = json_data[i]['itemId']
    #     # print(itemId)
    #     # print(list1)
    #     if str(itemId) in list1:
    #         nd += 1
    #         print("不执行请求")
    #     else:
    #         faqi(itemId, key4)
    #         d += 1
    #
    # print('执行删除%d次\n不执行删除%d次' % (d, nd))
    # # id = '255715692576771'
    # # faqi(id, key4)


    # for i in range(m, n):
    #     list1 = askUrl(i, j)
    #     list3 = uplist(list1, db_file1)
    #     if not list3:
    #         print("数据库新增数据0条")
    #     else:
    #         row = insert_mult_data(list3, db_file1)
    #         print("数据库新增数据%d条\n" % row)
    #     print("开始执行项目报备数据")
    # main1(token)


#请求商品清单
def askUrl(i, j, key):  # key为请求协议商品/基础商品
    print('正在进行一次请求')
    url = 'https://www.zcygov.cn/agreement/goods/'+key+'/paging'
    data = {
        'timestamp': 1614143524,
        'pageNo': i,
        'pageSize': j,
    }
    if key == 'protocol':  # 如果请求'协议商品'，需要添加参数
        data['status'] = '-1'  # 空：全部；1：上架；-1：下架；-2：冻结

    r = requests.get(url, params=data, headers=headers, cookies=cookies)
    r.encoding = 'utf-8'
    # print(r.text)
    print("每页请求%d条，请求%d页,结果total为：%s" % (j, i, r.json()['total']))
    # print("请求结果error为：%s" % r.json()['error'])
    # print("请求结果原文：%s" % r.json()['result'])
    # print("total：%s" % r.json()['result']['total'])
    # print("请求数据为（列表）：%s" % r.json()['result']['data'])
    list1 = r.json()['data']
    print('每次请求的数据类型为%s' % type(list1))
    print('每次请求的数据长度为%d\n' % len(list1))
    return list1

# 组批量删除、下架的列表
def pinjie(id, data):

    if key == 'UNDER_SHELF':
        data = [{'applyType': "GOODS_UNDER_SHELF_APPLY", "itemId": id, "source": 5, "enclosureDTO": {}}]
    # 删除
    elif key == 'DELETE':
        data = [{"applyType": "GOODS_DELETE_APPLY", "itemId": id, "source": 5}]




# 发起批量下架/删除
def faqi(id, key):
    url = 'https://www.zcygov.cn/agreement/goods/agreementItem/batchApply'
    # 下架
    if key == 'UNDER_SHELF':
        data = [{'applyType': "GOODS_UNDER_SHELF_APPLY", "itemId": id, "source": 5, "enclosureDTO": {}}]
    # 删除
    elif key == 'DELETE':
        data = [{"applyType": "GOODS_DELETE_APPLY", "itemId": id, "source": 5}]
    data = json.dumps(data)
    # print(data)
    r = requests.post(url, data=data, headers=headers, cookies=cookies)
    r.encoding = 'utf-8'
    print(r.text)


if __name__ == "__main__":  # 当程序执行时
    print('Start：开始执行程序\n')
    time_start = time.time()
    main()
    t = time.time() - time_start
    print(f'End：程序执行完毕，总共执行时间：{int(t / 60)}分 {int(t % 60)}秒!')