# coding=utf-8
import openpyxl
import requests
import time
import random
import json

# 不需要变更的配置
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
# timestamp = 1614143524

# 通用配置
cookies = {'shiroCookie': 'd497c834-2e22-4199-8a7f-1b76b2492700'}
pageNo_s = 0  # 起始页
pageNo_e = 70  # 终止页
pageSize = 100  # 每页大小
time_now = time.strftime("%Y%m%d-%H%M", time.localtime())
wfile_name = f'./设备库{time_now}.json'  # 写入文件名


# 定义主函数
def main():
    lst = askUrl2(pageNo_s, pageNo_e, pageSize)


# 请求商品审核清单
def askUrl1(pageNo_s, pageNo_e, pageSize):
    print(f'开始请求\n起始页：{pageNo_s}  终止页：{pageNo_e}  每页大小：{pageSize}')
    url = 'https://gboss.pinming.cn/device/list'
    list_all = []  # 定义空列表，用于接收数据并写入
    for pageNo in range(pageNo_s, pageNo_e + 1):
        page = pageNo*pageSize
        data = {'offset': page,
                'limit': pageSize}
        print(data)
        r = requests.post(url, params=data, headers=headers, cookies=cookies)
        r.encoding = 'utf-8'
        # print(r.text)
        list1 = r.json()['rows']
        list_all += list1
        time.sleep(random.randint(3, 5))
        print(f'每页请求{pageSize}条，请求{pageNo}页')
    print(f'请求完毕,总共有{len(list_all)}条数据')
    cucun(list_all)
    # return list_all


def askUrl2(pageNo_s, pageNo_e, pageSize):
    print(f'开始请求\n起始页：{pageNo_s}  终止页：{pageNo_e}  每页大小：{pageSize}')
    url = 'http://gboss.pinming.cn/warehouseDevice/list'
    list_all = []  # 定义空列表，用于接收数据并写入
    for pageNo in range(pageNo_s, pageNo_e + 1):
        page = pageNo*100
        if page == 300:
            print('跳过')
        else:
            data = {'offset': page,
                    'limit': pageSize}
            print(data)
            r = requests.post(url, params=data, headers=headers, cookies=cookies)
            r.encoding = 'utf-8'
            print(r.text)
            list1 = r.json()['rows']
            list_all += list1
            time.sleep(random.randint(1, 2))
            print(f'每页请求{pageSize}条，请求{pageNo}页')
    print(f'请求完毕,总共有{len(list_all)}条数据')
    cucun(list_all)
    # return list_all


def cucun(list_all):
    print(f'正在储存数据，文档名为:{wfile_name}')
    with open(wfile_name, 'w') as f:
        json.dump(list_all, f, ensure_ascii=False)

if __name__ == "__main__":  # 当程序执行时
    print('Start：开始执行程序\n')
    time_start = time.time()
    main()
    t = time.time() - time_start
    print(f'End：程序执行完毕，总共执行时间：{int(t / 60)}分 {int(t % 60)}秒!')