import requests
import json
import time
import random

pageNo_s = 1  # 起始页
pageNo_e = 2  # 终止页
pageSize = 100  # 每页大小

wfile_name = './非实名制人员.json'  # 写入文件名
rfile_name = './非实名制人员.json'  # 读取文件名
token = '1d8dbbb982334d9894ced476d4d712b9'
headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'x-access-token': token,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}


# 定义主函数
def main():
    # lst = askUrl(pageNo_s, pageNo_e, pageSize,)
    with open(rfile_name, 'r', encoding='utf-8') as f:
        list_data = json.load(f)
        for i in range(len(list_data)):
            signId = list_data[i]['signId']
            # print(signId)
            deleteUnSign(signId)

# 请求非实名制人员清单
def askUrl(pageNo_s, pageNo_e, pageSize):
    # print(f'开始请求--商品审核状态为（{ll[status]}）清单\n起始页：{pageNo_s}终止页：{pageNo_e}每页大小：{pageSize}')
    list_all = []
    for pageNo in range(pageNo_s, pageNo_e + 1):
        url = f'http://115.233.209.232:9000/api/realname/sign/{pageNo}/{pageSize}/unWorkerSignList'
        data = {"projectId": "448"}
        r = requests.post(url, json=data, headers=headers)
        r.encoding = 'utf-8'
        # print(r.text)
        list1 = r.json()['data']['list']
        list_all += list1
    #     print(f'每页请求{pageSize}条，请求{pageNo}页,结果success为：{r.json()["success"]},total:{r.json()["result"]["total"]}')
    # print(f'请求完毕,总共有{len(list_all)}条数据')
    # print(f'正在储存数据，文档名为:{wfile_name}')
    with open(wfile_name, 'w') as f:
        json.dump(list_all, f, ensure_ascii=False)
    return list_all


# 发起非实名制人员记录清楚
def deleteUnSign(signId):
    url = f'http://115.233.209.232:9000/api/realname/sign/deleteUnSign/{signId}'
    # data = json.dumps(data)
    r = requests.post(url, headers=headers)
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
    start = time.time()
    main()
    end = time.time()
    t = end - start
    if t < 120:
        print('End：程序执行完毕，总共执行时间：%d秒' % round(t, 2))  # 取整，保留两位小数
    else:
        t = t / 60
        print('End：程序执行完毕，总共执行时间：%d分钟' % round(t, 2))
