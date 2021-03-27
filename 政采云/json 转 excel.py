import json
import tablib


def json_to_xls(jname, xname):
    # 获取ｊｓｏｎ数据
    with open(jname, 'r') as f:
        rows = json.load(f)
        # print(rows)

    # 将json中的key作为header, 也可以自定义header（列名）
    header = tuple([i for i in rows[0].keys()])

    data = []
    # 循环里面的字典，将value作为数据写入进去
    for row in rows:
        body = []
        for v in row.values():
            body.append(str(v))
        data.append(tuple(body))

    data = tablib.Dataset(*data, headers=header)

    open(xname, 'wb').write(data.xls)


json_to_xls('/Users/zml/PycharmProjects/pythonProject5/gboss/设备库20210303-2251.json', './data3.xls')