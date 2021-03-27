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
cookies = {'SESSION': 'Y2MxOTQ4MGEtNzY3OS00MmRjLWI2YjQtMDg2ZGI3NzUxMzUx'}
pageNo_s = 1  # 起始页
pageNo_e = 1  # 终止页
pageSize = 100  # 每页大小
time_now = time.strftime("%Y%m%d-%H%M", time.localtime())
wfile_name = f'./数据/商品审核/基础商品-下架{time_now}.json'  # 写入文件名
rfile_name = './数据/商品审核/基础商品-下架20210323-2156.json'  # 读取文件名
# 商品审核，所需的配置
status = '1'  # null：全部，1：审核中，3：驳回，4：通过

key1 = 'protocol'  # 基础商品：'channel'    协议商品：'protocol'
key3 = 'DELETE'  # 下架功能：'UNDER_SHELF'  删除功能：'DELETE'
id = '262107157598208'
data = [{'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}, {'applyType': 'GOODS_DELETE_APPLY', 'itemId': 262107358937099, 'source': 5}]
def faqi(data):
    url = 'https://www.zcygov.cn/agreement/goods/agreementItem/batchApply'
    data = json.dumps(data)
    # print(data)
    r = requests.post(url, data=data, headers=headers, cookies=cookies)
    r.encoding = 'utf-8'
    print(r.text)



with open('./数据/商品审核/已经关联协议商品20210324-2138.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)
    print(len(json_data))
    print(json_data[0]['channelItemId'])


'''
协议商品你的基础id：channelItemId
基础商品里的商品id：itemId

关联协议：
"agChannelGoodsRelProtocols": [
                {
                    "protocolId": 33683,
                    "protocolName": "浙江省网上超市全省一张网-义乌市鑫榜办公用品商行"
                }
            ]


'''
