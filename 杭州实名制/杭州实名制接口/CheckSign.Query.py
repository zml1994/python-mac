# 330109191123010160
# 项目名称：萧政储出（2017）12号地块居住项目二标段
# 施工单位：浙江杰立建设集团有限公司
# appid：330109191123010160
# 项目编码：330109191123010160
# 密钥：G85qF5JP-7PO#Mx#JT#mmaeOJ6tcf!v-
# 平台地址：http://115.233.209.232:9000/
# 项目账号：13375717532
# 密码：Aa123456
import random
import time
import hashlib
import requests
import json

appid = "330109191123010160"
data = {}
data = json.dumps(data)
format = "json"
method = "CheckSign.Query"
nonce = random.randint(0, 999999)
timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
version = 1.1
appsecret = "G85qF5JP-7PO#Mx#JT#mmaeOJ6tcf!v-"
test = 'appid=%s&data=%s&format=json&method=%s&nonce=%s&timestamp=%s&version=%s' % (appid, data, method, nonce,
                                                                                    timestamp, version)
test1 = '%s&appsecret=%s' % (test, appsecret)
test1 = test1.lower()
sign = hashlib.sha256(test1.encode('utf-8')).hexdigest()
# print(test1)
# print(sign)
test2 = '%s&sign=%s' % (test, sign)
# print(test2)
url = "http://115.233.209.232:9089/open.api"
# # res = requests.get(url)
# print(res.text)
# headers = {'Content-Type': 'application/x-www-form-urlencoded'}
datas = {"appid": appid,
         "data": data,
         "format": format,
         "method": method,
         "nonce": nonce,
         "timestamp": timestamp,
         "version": version,
         "sign": sign
         }

res = requests.post(url, data=datas)
print(res.text)
# print(res.)

