import requests
import json
import time
import random

m = 1  # 起始页码
n = 50  # 终止页
j = 100  # 每页大小
# cookies = dict(SESSION='ZDM5NTEwN2EtZGJlMS00MTJjLTk1OWQtOTA2ZGE5NWY0OWJm')
cookies = {'SESSION': 'ZWI0ZGVmMGMtOTY2YS00ZWJjLWFhOGMtMmUyM2E2ZWQwYTBl'}
headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}


# 定义主函数
def main():
    list_all = []
    for i in range(m, n + 1):
        list_return = askUrl(i, j)
        list_all += list_return
        print(len(list_all))
    with open('批量上架.json', 'w') as f:
        json.dump(list_all, f, ensure_ascii=False)

    # 打开json数据，批量发布
    with open('批量上架.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        max_count = len(json_data)
        print(f'总共含有{max_count}条数据')
        k = 0  # 起始更改值
        while k < max_count:
            list1 = []
            data = json_data[k:k + 40]
            for i in range(len(data)):
                list1.append(data[i]['itemId'])
            # print(list1)
            # list2 = json.dumps(list1)
            # print(list2)
            batchAssociateProtocol(list1)
            time.sleep(random.randint(1, 3))  # 随机睡眠1-4秒，用于减少高频率请求
            print("\t正在批量发布第%d至%d条数据" % (k, k + 40))
            k = k + 40

    # # 打开json数据，批量改价
    # with open('number2.json', 'r', encoding='utf-8') as f:
    #     json_data = json.load(f)
    #     max_count = len(json_data)
    #     k = 0   # 起始更改值
    #     while k < max_count:
    #         data = json_data[k:k + 40]
    #         data = {"type": 2, "items": data, "operation": {"operationType": 5, "operationValue": 94}}
    #         batchUpdate(data)
    #         print("正在修改第%d至%d条数据" % (k, k+40))
    #         k = k + 40

    # for i in json_data
    # data = {"type": 2, "items": json_data, "operation": {"operationType": 5, "operationValue": 50}}
    # # print(type(json_data))
    # # print(type(data))
    # batchUpdate(data)

    # # 循环撤销
    # for i in range(len(json_data)+1):
    #     id = json_data[i]['id']
    #     print(id)
    #     batchUpdate(id)
    # id = '64671779'
    # revokeApply(id)
    # 使用json load读取文件内容，然后可以直接用列表或者字典的方式去操作con这个变量
    # f = json.loads(content)
    # data = json.dumps(list, ensure_ascii=False)
    # f.write(data.encode('utf-8'))
    # init_db(db_file1)
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


# 请求商品清单
def askUrl(i, j):
    url = 'https://middle.zcygov.cn/distributors/supplier/item/search'
    data = {
        'timestamp': 1614242267,
        'pageNo': i,
        'pageSize': j,
        'layer': '28'
    }
    r = requests.get(url, params=data, headers=headers, cookies=cookies)
    r.encoding = 'utf-8'
    # print(r.text)
    print("每页请求%d条，请求%d页,结果success为：%s" % (j, i, r.json()['success']))
    # print("请求结果原文：%s" % r.json()['result'])
    print("total：%s" % r.json()['result']['total'])
    print("totalPage：%s" % r.json()['result']['totalPage'])
    # print("请求数据为（列表）：%s" % r.json()['result']['data'])
    list1 = r.json()['result']['data']
    print(type(list1))
    return list1


# 发起改价
def batchUpdate(data):
    url = 'https://middle.zcygov.cn/distributors/supplier/item/batchUpdate'
    data = json.dumps(data)
    r = requests.post(url, data=data, headers=headers, cookies=cookies)
    r.encoding = 'utf-8'
    print(r.text)


# 批量发布
def batchAssociateProtocol(list1):
    data = {"protocolId": "33683", "itemIds": list1}
    # print(data)
    url = 'https://middle.zcygov.cn/distributors/supplier/item/batchAssociateProtocol'
    data = json.dumps(data)
    r = requests.post(url, data=data, headers=headers, cookies=cookies)
    r.encoding = 'utf-8'
    print(r.text)


if __name__ == "__main__":  # 当程序执行时
    print('Start：开始执行程序\n')
    time_start = time.time()
    main()
    t = time.time() - time_start
    print(f'End：程序执行完毕，总共执行时间：{int(t / 60)}分 {int(t % 60)}秒!')
