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

url = "http://115.233.209.232:9089/open.api?"
appid = "330109191123010160"
data = {
    "pageIndex": 0,
    "pageSize": 10,
    "projectCode": appid
}
data = json.dumps(data)
format = "json"
method = "Project.Query"
nonce = random.randint(0, 999999)
timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
version = '1.0'
appsecret = "G85qF5JP-7PO#Mx#JT#mmaeOJ6tcf!v-"
test = 'appid=%s&data=%s&format=%s&method=%s&nonce=%s&timestamp=%s&version=%s' % (appid, data, format, method, nonce,
                                                                                    timestamp, version)  # 拼接签名参数
test1 = '%s&appsecret=%s' % (test, appsecret)  # 拼接密钥
test1 = test1.lower()  # 转化成小写
sign = hashlib.sha256(test1.encode('utf-8')).hexdigest()  # 生成签名
test2 = '%s&sign=%s' % (test, sign)  # 生成请求参数
print(test2)
datas = {
         "appid": appid,
         "data": data,
         "format": format,
         "method": method,
         "nonce": nonce,
         "timestamp": timestamp,
         "version": version,
         "sign": sign
         }
print(datas)

res = requests.post(url, data=datas)
print(res.text)
