import random
import time
import hashlib
import requests
import json

appid = "330110200307020004"
appsecret = "kg3QioEXfUk5eq9zSHaXF1-EUaPGA?=r"
data = {}


# 异步查询接口 待调试
def AsyncHandleResult_Query(data):
    # 1、确认需要传送的data数据
    data1 = {
        'requestSerialCode': '' # 请求序列编码,string
    }
    data.update(data1)

    # 2、构建完整的data数据
    data = todata(data)  # 构建完整的data

    # 3、根据接口不同，更新data字段
    data['method'] = 'AsyncHandleResult.Query'  # 字典中更新调用方法

    # 4、根据data，调用post请求
    post(data, '查询考勤接口')

# 查询考勤接口
def WorkerAttendance_Query(data):
    # 1、确认需要传送的data数据
    data1 = {
        'pageIndex': 0,
        'pageSize': 50,
        'projectCode': appid,
        'date': '2021-01-14',  # 考勤日期，格式 yyyy-MM-dd
        'teamSysNo': '',  # 班组编号
        'idCardType': '01',  # 证件类型，参考人员证件类型字典表
        'idCardNumber': 'cZh1f4zjcRM6ZL7BYO5gviecjx+DlnIpdzGSzSm5Y1s='  # 证件号码，AES
    }
    data.update(data1)

    # 2、构建完整的data数据
    data = todata(data)  # 构建完整的data

    # 3、根据接口不同，更新data字段
    data['method'] = 'WorkerAttendance.Query'  # 字典中更新调用方法

    # 4、根据data，调用post请求
    post(data, '查询考勤接口')

# 查询进/退场接口
def WorkerEntryExit_Query(data):
    # 1、确认需要传送的data数据
    data1 = {
        'pageIndex': 0,
        'pageSize': 50,
        'projectCode': appid,
        'corpCode': '',  # 社会信用代码，如果无统一社会信用代码，则用组织机构代码
        'corpName': '',  # 企业名称
        'teamSysNo': '',  # 班组编号
        'idCardType': '01',  # 证件类型，参考人员证件类型字典表
        'idCardNumber': '4xrHG8IQIYLgKzHJLJMncx79UUWTEH6NPRaRlg3pzbg='  # 证件号码，AES
    }
    data.update(data1)

    # 2、构建完整的data数据
    data = todata(data)  # 构建完整的data

    # 3、根据接口不同，更新data字段
    data['method'] = 'WorkerEntryExit.Query'  # 字典中更新调用方法

    # 4、根据data，调用post请求
    post(data, '查询进/退场接口')

# 查询工人信息接口
def ProjectWorker_Query(data):
    # 1、确认需要传送的data数据
    data1 = {
        'pageIndex': 0,
        'pageSize': 50,
        'projectCode': appid,
        'corpCode': '',  # 社会信用代码，如果无统一社会信用代码，则用组织机构代码
        'corpName': '杭州汉运建筑劳务有限公司',  # 企业名称
        'teamSysNo': '64780',  # 班组编号
        'idCardType': '01',  # 证件类型，参考人员证件类型字典表
        'idCardNumber': 'cZh1f4zjcRM6ZL7BYO5gviecjx+DlnIpdzGSzSm5Y1s='  # 证件号码，AES
    }
    data.update(data1)

    # 2、构建完整的data数据
    data = todata(data)  # 构建完整的data

    # 3、根据接口不同，更新data字段
    data['method'] = 'ProjectWorker.Query'  # 字典中更新调用方法

    # 4、根据data，调用post请求
    post(data, '查询工人信息接口')

# 查询班组信息
def Team_Query(data):
    # 1、确认需要传送的data数据
    data1 = {
        'pageIndex': 0,
        'pageSize': 50,
        'teamSysNo': '',  # 班组编号
        'projectCode': appid,
        'teamName': '',  # 班组名称
        'corpCode': '',  # 社会信用代码，如果无统一社会信用代码，则用组织机构代码
        'corpName': '杭州汉运建筑劳务有限公司'  # 企业名称
    }
    data.update(data1)

    # 2、构建完整的data数据
    data = todata(data)  # 构建完整的data

    # 3、根据接口不同，更新data字段
    data['method'] = 'Team.Query'  # 字典中更新调用方法

    # 4、根据data，调用post请求
    post(data, '查询班组信息')

# 查询参建接口
def ProjectSubContractor_Query(data):
    # 1、确认需要传送的data数据
    data1 = {
        'pageIndex': 1,
        'pageSize': 50,
        'projectCode': appid,
        'corpCode': '',  # 社会信用代码，如果无统一社会信用代码，则用组织机构代码
        'corpName': ''  # 企业名称
    }
    data.update(data1)

    # 2、构建完整的data数据
    data = todata(data)  # 构建完整的data

    # 3、根据接口不同，更新data字段
    data['method'] = 'ProjectSubContractor.Query'  # 字典中更新调用方法

    # 4、根据data，调用post请求
    post(data, '查询参建接口')


# 查询项目信息接口
def Project_Query(data):
    # 1、确认需要传送的data数据
    data1 = {
        'pageIndex': 0,
        'pageSize': 10,
        'projectCode': appid,
        'contractorCorpCode': '',
        'contractorCorpName': ''
    }
    data.update(data1)

    # 2、构建完整的data数据
    data = todata(data)  # 构建完整的data

    # 3、根据接口不同，更新data字段
    data['method'] = 'Project.Query'  # 字典中更新调用方法

    # 4、根据data，调用post请求
    post(data, '查询项目信息接口')


# 验证签名方法（appid和密钥的正确）
def CheckSign_Query(data):
    # 1、确认需要传送的data数据

    # 2、构建完整的data数据
    data = todata(data)

    # 3、根据接口不同，更新data字段
    data['version'] = '1.1'  # 字典中更新版本号
    data['method'] = 'CheckSign.Query'  # 字典中更新调用方法

    # 4、根据data，调用post请求
    post(data, '验证签名方法')


# 添加签名并请求
def post(data, API_Name):
    url = "http://115.233.209.232:9089/open.api"  # 杭州市的对接地址
    data['sign'] = sign(data)  # 生成签名并在字典中添加
    # print('签名后的数据字典：%s' % data)
    res = requests.post(url, data=data)
    print('%s,调用结果：%s\n' % (API_Name, res.text))


# 传入参数及密钥生成签名
def sign(data):
    str = pj(data).lower()  # 调用拼接函数并转换小写
    sign = hashlib.sha256(str.encode('utf-8')).hexdigest()  # 生成签名
    return sign


# 根据字典用&拼接
def pj(data):
    for key, valur in data.items():
        if key == "appid":  # 字典的前提是appid开头，需要优化
            str = key + "=" + valur
        else:
            str = str + "&" + key + "=" + valur
    return str


# 构建完整的data方法
def todata(data):
    data = json.dumps(data)  # 对data进行json格式化
    data = {'appid': appid,
            'data': data,
            'format': "json",
            'method': "",  # 方法，调用时添加
            'nonce': str(random.randint(0, 999999)),  # 生成随机数并转换成字符串
            'timestamp': time.strftime("%Y%m%d%H%M%S", time.localtime()),  # 生成时间戳,
            'version': "1.0",
            'appsecret': appsecret
            }
    return data


if __name__ == '__main__':
    # CheckSign_Query(data)
    # Project_Query(data)  # 查询项目信息
    # ProjectSubContractor_Query(data)  # 查询参建
    # Team_Query(data)  # 查询班组
    # ProjectWorker_Query(data)  # 查询工人
    # WorkerEntryExit_Query(data)  # 查询进退场
    WorkerAttendance_Query(data)  # 查询考勤