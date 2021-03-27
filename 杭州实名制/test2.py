import requests


def askUrl(url,data):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-access-token': 'e21e2a2ed5864572ba7eca602554e8d2'}
    # data = json.dumps(data)   #  序列化成jsong
    r = requests.post(url=url, json=data, headers=headers)
    r.encoding = 'utf-8'
    print(r.json())
    print(r.text)
    # print("post执行状态码：%s" % r.json()['code'])
    # print("post执行结果：%s" % r.json()['msg'])
    # print("post本页数据总数：%s" % r.json()['data']['currentPageSize'])
    # print("页码：%s" % r.json()['data']['pageNum'])
    # print("每页大小：%s" % r.json()['data']['pageSize'])
    # print("总共%s页" % r.json()['data']['totalPage'])
    # print("项目总数总数：%s" % r.json()['data']['total'])
    # data = r.json()['data']
    # list1 = data['list']
    # return list1


askUrl(url1, data4)