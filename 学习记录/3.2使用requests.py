import requests
import json
url = 'http://115.233.209.232:9000/api/project/findProject/1/10'
headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'x-access-token': '868e7110cc374abfa369638bc9aaf149'

}
data = {}  # 空字典
# data = json.dumps(data)   #  序列化成jsong
r = requests.post(url=url, json=data, headers=headers)
r.encoding= 'utf-8'
print(type(r))
# print(r.json())
print(r.json()['code'])
print(r.json()['msg'])

data = r.json()['data']
list = data['list']
print(len(list))
for i in range(len(list)):
    print(type(list[i]))
# print(json.loads(r))