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
appid_hz = "330109191123010813"
appsecret_hz = "FEkeMj!!RZcwgSW?A-+j1QX+0DM?oqnZ"
# 偏移量 FEkeMj!!RZcwgSW?
appid_xs = "330109200317010026"
appsecret_xs = "9EzjVHx15nr9K!np$pfY$vTJP6OM0Zu="
# 偏移量 9EzjVHx15nr9K!np
appid = appid_hz
appsecret = appsecret_hz
url_hz = "http://115.233.209.232:9089/open.api?"
url_xs = "http://xiaoshan-rn-api.pinming.cn/open.api?"
data = {
    "pageIndex": 0,
    "pageSize": 50,
    "projectCode": appid,
    # "idCardNumber":"Phzs4hrbu4pgHp1WpQkXH2PzdeTRgeFl8+y+jvWaOOY="
    "idCardNumber": "QxLpI/X/9sPoW/4Tpq9pQSH1jCJ3lnOl3uw/qw6mM4w="
   # "idCardNumber": ["QxLpI/X/9sPoW/4Tpq9pQSH1jCJ3lnOl3uw/qw6mM4w=", "Phzs4hrbu4pgHp1WpQkXH2PzdeTRgeFl8+y+jvWaOOY="]
    # "corpName": "杭州市滨江区农村多层住宅建设管理中心"
}
data = json.dumps(data)
format = "json"
method = "ProjectWorker.Query"
nonce = random.randint(0, 999999)
timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
version = '1.0'
test = 'appid=%s&data=%s&format=%s&method=%s&nonce=%s&timestamp=%s&version=%s' % (appid, data, format, method, nonce,
                                                                                    timestamp, version)  # 拼接签名参数
test1 = '%s&appsecret=%s' % (test, appsecret)  # 拼接密钥
test1 = test1.lower()  # 转化成小写
sign = hashlib.sha256(test1.encode('utf-8')).hexdigest()  # 生成签名
test2 = '%s&sign=%s' % (test, sign)  # 生成请求参数
print(test2,end="\n\n")
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
print(datas,end="\n\n")
url = url_hz
res = requests.post(url, data=datas)
print(res.text)
