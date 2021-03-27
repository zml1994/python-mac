import random
import time
import hashlib
import requests
import json
requestSerialCode = '5b3099d779ff4fb080218d0c6563ee6e'
def AsyncHandleResultQuery(requestSerialCode):
    appid = "330109191123010160"
    appsecret = "G85qF5JP-7PO#Mx#JT#mmaeOJ6tcf!v-"
    url = "http://115.233.209.232:9089/open.api?"
    data = {
            "requestSerialCode": requestSerialCode
        }
    data = json.dumps(data)
    format = "json"
    method = "AsyncHandleResult.Query"
    nonce = random.randint(0, 999999)
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    version = '1.0'
    test = 'appid=%s&data=%s&format=%s&method=%s&nonce=%s&timestamp=%s&version=%s' % (
    appid, data, format, method, nonce, timestamp, version)  # 拼接签名参数
    test1 = '%s&appsecret=%s' % (test, appsecret)  # 拼接密钥
    test1 = test1.lower()  # 转化成小写
    sign = hashlib.sha256(test1.encode('utf-8')).hexdigest()  # 生成签名
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
    res = requests.post(url, data=datas)
    print(res.json())


AsyncHandleResultQuery(requestSerialCode)