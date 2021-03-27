
url = 'http://115.233.209.232:9000/api/company/create'

data = {"corpCode": "123456789012345678",
        "handleCorpTypes": ["001"],
        "corpName": "1",
        "registerDate": "2021-01-14",
        "province": "河北省",
        "address": "1",
        "legalMan": "1",
        "city": "秦皇岛市",
        "county": "山海关区",
        "areaId": "130303",
        "corpTypeCodes": ["001"]}


def askUrl(url,data):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-access-token': '1b6a6f33bdb14c7889dc05e42eb2e646'}
    # data = json.dumps(data)   #  序列化成jsong
    r = requests.post(url=url, json=data, headers=headers)
    r.encoding = 'utf-8'
    print(r.json())
    print(r.text)


askUrl(url, data)