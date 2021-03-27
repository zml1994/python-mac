# coding=utf-8
import openpyxl
import requests
import time
import random
import json

# 不需要变更的配置
headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
timestamp = 1614143524

# 通用配置
cookies = {'SESSION': 'YWJlYTY4YzUtNmY4NC00NTgxLThkOGMtNTE4Y2QxMWNmMzAy'}
pageNo_s = 1  # 起始页
pageNo_e = 64 # 终止页
pageSize = 40  # 每页大小
time_now = time.strftime("%Y%m%d-%H%M", time.localtime())
wfile_name = f'./数据/商品审核/已经关联协议商品{time_now}.json'  # 写入文件名
rfile_name = f'./数据/商品审核/基础商品{time_now}.json'  # 读取文件名
# 商品审核，所需的配置
status = '1'  # null：全部，1：审核中，3：驳回，4：通过

# 发布商品管理
key1 = 'channel'  # 基础商品：'channel'    协议商品：'protocol'
key3 = 'DELETE'  # 下架功能：'UNDER_SHELF'  删除功能：'DELETE'


# 定义主函数
def main():
    # 请求审核清单列表
    # lst = askUrl_his(pageNo_s, pageNo_e, pageSize, status)

    # 对json中的数据，发起撤销。需要提供id
    # with open(rfile_name, 'r', encoding='utf-8') as f:
    #     list_data = json.load(f)
    # # 循环撤销
    # n = len(list_data)
    # for i in range(n):
    #     id = list_data[i]['id']
    #     print(f'正在撤销第{i}条，id为：{id},总共有{n}条')
    #     revokeApply(id)

    # 请求商品管理
    # askUrl_paging(pageNo_s, pageNo_e, pageSize, key1)

    askUrl_pagingandd(pageNo_s, pageNo_e, pageSize, key1)


    # 读取商品id，循环删除
    # with open(rfile_name, 'r', encoding='utf-8') as f:
    #     json_data = json.load(f)
    # with open('已销售商品id', 'r') as f:
    #     list1 = f.read().split('\n')
    # list_d = ifpanduan(json_data, list1)
    # xunhuan(list_d)



# 循环请求删除
def xunhuan(list):
    m = 0
    while m < len(list):
        list1 = list[m:m + 40]
        m += 40
        faqi(listkkk(list1))



# 根据商品id文件，对list进行去除，再返回新的list
def ifpanduan(list, list1):
    l = len(list)
    d = 0
    nd = 0
    list_d = []
    for i in range(l):
        itemId = list[i]['itemId']
        if str(itemId) in list1:
            nd += 1
        else:
            list_d.append(itemId)
            d += 1
    return list_d





# 将列表转化成可以用于请求的列表 这里是删除功能
def listkkk(list):
    list1 = []
    dict = {"applyType": "GOODS_DELETE_APPLY", "itemId": '', "source": 5}
    for i in list:
        dict['itemId'] = i
        k = dict.copy()
        list1.append(k)
    return list1




# 请求商品审核清单
def askUrl_his(pageNo_s, pageNo_e, pageSize, status):
    ll = {'': '全部', '1': '审核中', '3': '驳回', '4': '通过'}
    print(f'开始请求--商品审核状态为（{ll[status]}）清单\n起始页：{pageNo_s}终止页：{pageNo_e}每页大小：{pageSize}')
    url = 'https://agreement.zcygov.cn/agreement/goods/his'
    list_all = []  # 定义空列表，用于接收数据并写入
    for pageNo in range(pageNo_s, pageNo_e + 1):
        data = {'timestamp': timestamp,
                'pageNo': pageNo,
                'pageSize': pageSize,
                'status': status}
        r = requests.get(url, params=data, headers=headers, cookies=cookies)
        r.encoding = 'utf-8'
        list1 = r.json()['result']['data']
        list_all += list1
        time.sleep(random.randint(0, 2))
        print(f'每页请求{pageSize}条，请求{pageNo}页,结果success为：{r.json()["success"]},total:{r.json()["result"]["total"]}')
    print(f'请求完毕,总共有{len(list_all)}条数据')
    cucun(list_all)
    return list_all


# 储存
def cucun(list_all):
    print(f'正在储存数据，文档名为:{wfile_name}')
    with open(wfile_name, 'w') as f:
        json.dump(list_all, f, ensure_ascii=False)


# 请求商品管理
def askUrl_paging(pageNo_s, pageNo_e, pageSize, key):  # key为请求协议商品/基础商品
    list_all = []  # 用于json写入的空列表
    for pageNo in range(pageNo_s, pageNo_e + 1):
        url = f'https://www.zcygov.cn/agreement/goods/{key}/paging'
        data = {
            'timestamp': timestamp,
            'pageNo': pageNo,
            'pageSize': pageSize,
        }
        if key == 'protocol':  # 如果请求'协议商品'，需要添加参数
            data['status'] = ''  # 空：全部  1：上架 -1：下架  -2：冻结
        r = requests.get(url, params=data, headers=headers, cookies=cookies)
        r.encoding = 'utf-8'
        print(f'每页请求{pageSize}条，请求{pageNo}页,结果total为：{r.json()["total"]}')
        list1 = r.json()['data']
        list_all += list1
        time.sleep(random.randint(0, 4))  # 随机睡眠0-4秒，用于减少高频率请求
    cucun(list_all)


# 请求并删除
def askUrl_pagingandd(pageNo_s, pageNo_e, pageSize, key):  # key为请求协议商品/基础商品
    list_all = []  # 用于json写入的空列表
    for pageNo in range(pageNo_e + 1, pageNo_s, -1):
        url = f'https://www.zcygov.cn/agreement/goods/{key}/paging'
        data = {
            'timestamp': timestamp,
            'pageNo': pageNo,
            'pageSize': pageSize,
        }
        if key == 'protocol':  # 如果请求'协议商品'，需要添加参数
            data['status'] = ''  # 空：全部  1：上架 -1：下架  -2：冻结
        r = requests.get(url, params=data, headers=headers, cookies=cookies)
        r.encoding = 'utf-8'
        print(f'每页请求{pageSize}条，请求{pageNo}页,结果total为：{r.json()["total"]}')
        list1 = r.json()['data']
        list2 = []
        for i in list1:
            if i['agChannelGoodsRelProtocols'] == []:
                list2.append(i['itemId'])
        print(len(list2))
        shanchu(list2)
                

def shanchu(list):
    url = 'https://www.zcygov.cn/agreement/goods/channelGoods/delete'
    data = json.dumps(list)
    r = requests.post(url, data=data, headers=headers, cookies=cookies)
    # r.encoding = 'utf-8'
    # print(f'商品撤销结果：{r.text}')



# 商品审核-发起撤销,逐个撤销，需要提供id
def revokeApply(id):
    url = 'https://agreement.zcygov.cn/agreement/goods/agreementItem/revokeApply'
    data = str(id)
    r = requests.post(url, data=data, headers=headers, cookies=cookies)
    r.encoding = 'utf-8'
    print(f'商品撤销结果：{r.text}')


# 商品管理 功能
def faqi(id_list):
    url = 'https://www.zcygov.cn/agreement/goods/agreementItem/batchApply'
    data = json.dumps(id_list)
    # print(data)
    r = requests.post(url, data=data, headers=headers, cookies=cookies)
    r.encoding = 'utf-8'
    print(f'请求结果如下\n{r.text}')


if __name__ == "__main__":  # 当程序执行时
    print('Start：开始执行程序\n')
    time_start = time.time()
    main()
    t = time.time() - time_start
    print(f'End：程序执行完毕，总共执行时间：{int(t / 60)}分 {int(t % 60)}秒!')
