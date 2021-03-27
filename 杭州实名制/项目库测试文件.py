# -*- coding: utf-8 -*-
import sqlite3


list =[{'address': '拱墅区', 'areaId': 330105005, 'builderLicenseNumber': '330101202012140302', 'buildingArea': 433.0, 'category': '02', 'categoryName': '市政公用工程', 'city': '杭州市', 'completeDate': '2022-04-01', 'contractorCorpNames': '浙江千日红市政园林工程有限公司', 'county': '拱墅区', 'govOrgId': 5, 'invest': 508.0064, 'lat': 30.3349, 'lng': 120.12918, 'orgName': '市本级', 'projectArea': '浙江省杭州市拱墅区拱宸桥街道', 'projectCode': '330105210113020001', 'projectId': 8078, 'projectName': '运河新城单元（运河湾城市设计范围）规划支路四（通益路-规划支路九）道路工程', 'projectStatus': '006', 'projectStatusName': '未开工', 'province': '浙江省', 'small': 0, 'startDate': '2021-11-01', 'street': '拱宸桥街道'}, {'address': '丁兰街道皋城村皋亭山景区', 'areaId': 330104013, 'builderLicenseNumber': '330101201906140101', 'category': '01', 'categoryName': '房屋建筑工程', 'city': '杭州市', 'contractorCorpNames': '浙江正品建设工程有限公司', 'county': '江干区', 'govOrgId': 5, 'lat': 30.38831, 'lng': 120.23067, 'orgName': '市本级', 'projectArea': '浙江省杭州市江干区丁兰街道', 'projectCode': '330106200307010002', 'projectId': 6067, 'projectName': '杭州龙居寺（处所）扩建及配套设施项目一期（四众安养区）', 'projectStatus': '003', 'projectStatusName': '在建', 'province': '浙江省', 'reformCode': '2017-330104-47-01-020757-001', 'relationBuilderLicenseNumber': '', 'small': 0, 'startDate': '2021-07-21', 'street': '丁兰街道'}, {'address': '杭州市拱墅区运河新城单元', 'areaId': 330105003, 'builderLicenseNumber': '330101202012140102', 'category': '02', 'categoryName': '市政公用工程', 'city': '杭州市', 'completeDate': '2021-07-31', 'contractorCorpNames': '浙江千日红市政园林工程有限公司', 'county': '拱墅区', 'govOrgId': 5, 'invest': 156.8308, 'lat': 30.33759, 'lng': 120.13097, 'orgName': '市本级', 'projectArea': '浙江省杭州市拱墅区小河街道', 'projectCode': '330105210113020002', 'projectId': 8079, 'projectName': '运河新城单元（运河湾城市设计范围）规划支路九（规划支路四-规划支路五）道路工程', 'projectStatus': '006', 'projectStatusName': '未开工', 'province': '浙江省', 'small': 1, 'startDate': '2021-03-01', 'street': '小河街道'}, {'address': '杭州市拱墅区运河新城单元，东至拱康路沿线绿化带，南至规划支路，西至运河新城单元C-R21-07地块', 'areaId': 330105008, 'builderLicenseNumber': '330105202012280301', 'category': '01', 'categoryName': '房屋建筑工程', 'city': '杭州市', 'completeDate': '2023-10-17', 'contractorCorpNames': '浙江新盛建设集团有限公司', 'county': '拱墅区', 'govOrgId': 10, 'invest': 25177.5004, 'lat': 30.33854, 'lng': 120.14629, 'orgName': '拱墅区', 'projectArea': '浙江省杭州市拱墅区上塘街道', 'projectCode': '330105210118010011', 'projectId': 8107, 'projectName': '运河新城单元C-A33-01地块30班小学（瓜山小学）', 'projectStatus': '006', 'projectStatusName': '未开工', 'province': '浙江省', 'small': 0, 'startDate': '2021-03-01', 'street': '上塘街道'}, {'address': '临浦镇', 'areaId': 330109105, 'builderLicenseNumber': '330109202011040101', 'category': '01', 'categoryName': '房屋建筑工程', 'city': '杭州市', 'completeDate': '2021-09-30', 'contractorCorpNames': '浙江汇宇建设有限公司', 'county': '萧山区', 'govOrgId': 14, 'invest': 998.0, 'lat': 30.07901, 'lng': 120.26987, 'orgName': '萧山区', 'projectArea': '浙江省杭州市萧山区临浦镇', 'projectCode': '330109201106010001', 'projectId': 7719, 'projectName': '年产150万套家用类电机生产线项目', 'projectStatus': '003', 'projectStatusName': '在建', 'province': '浙江省', 'small': 0, 'startDate': '2021-01-21', 'street': '临浦镇'}, {'address': '临浦镇', 'areaId': 330109105, 'builderLicenseNumber': '330109202009100101', 'buildingArea': 11377.0, 'category': '01', 'categoryName': '房屋建筑工程', 'city': '杭州市', 'completeDate': '2021-08-30', 'contractorCorpNames': '浙江汇宇建设有限公司', 'county': '萧山区', 'govOrgId': 14, 'invest': 1518.1928, 'lat': 30.08119, 'lng': 120.26974, 'orgName': '萧山区', 'projectArea': '浙江省杭州市萧山区临浦镇', 'projectCode': '330109200925010016', 'projectId': 7563, 'projectName': '2000吨有机硅工业电子密封胶:LED灌封胶（生产分装）', 'projectStatus': '003', 'projectStatusName': '在建', 'province': '浙江省', 'small': 0, 'startDate': '2021-01-21', 'street': '临浦镇'}, {'address': '桐庐县凤翔路与凤龙路交叉口', 'areaId': 330122005, 'builderLicenseNumber': '330122202011060201', 'category': '01', 'categoryName': '房屋建筑工程', 'city': '杭州市', 'completeDate': '2022-01-31', 'contractorCorpNames': '浙江宏超建设集团有限公司', 'county': '桐庐县', 'govOrgId': 17, 'invest': 7395.5717, 'lat': 29.82878, 'lng': 119.75191, 'orgName': '桐庐县', 'projectArea': '浙江省杭州市桐庐县凤川街道', 'projectCode': '330122210119010001', 'projectId': 8111, 'projectName': '桐庐电力开发有限公司智能电网系统研发制造项目', 'projectStatus': '003', 'projectStatusName': '在建', 'province': '浙江省', 'small': 0, 'startDate': '2021-01-20', 'street': '凤川街道'}, {'address': '董家路', 'areaId': 330122005, 'builderLicenseNumber': '330122202012240101', 'category': '01', 'categoryName': '房屋建筑工程', 'city': '杭州市', 'completeDate': '2021-08-15', 'contractorCorpNames': '杭州开沅建设有限公司', 'county': '桐庐县', 'govOrgId': 17, 'invest': 1500.0, 'lat': 29.82184, 'lng': 119.73184, 'orgName': '桐庐县', 'projectArea': '浙江省杭州市桐庐县凤川街道', 'projectCode': '330122210120010001', 'projectId': 8119, 'projectName': '浙江瑞能通信科技股份有限公司厂房扩建', 'projectStatus': '003', 'projectStatusName': '在建', 'province': '浙江省', 'small': 0, 'startDate': '2021-01-20', 'street': '凤川街道'}, {'address': '分水镇南门3-3号地块', 'areaId': 330122109, 'builderLicenseNumber': '330122202011180201', 'category': '01', 'categoryName': '房屋建筑工程', 'city': '杭州市', 'completeDate': '2022-05-31', 'contractorCorpNames': '杭州港湾建设有限公司', 'county': '桐庐县', 'govOrgId': 17, 'invest': 3300.0, 'lat': 29.93018, 'lng': 119.43999, 'orgName': '桐庐县', 'projectArea': '浙江省杭州市桐庐县分水镇', 'projectCode': '330122210120010002', 'projectId': 8120, 'projectName': '桐庐骨伤科医院康养大厦建设项目', 'projectStatus': '003', 'projectStatusName': '在建', 'province': '浙江省', 'small': 0, 'startDate': '2021-01-20', 'street': '分水镇'}, {'address': '杭州市拱墅区半山街道， 320国道以西、刘文路以东、临一路以南', 'areaId': 330105011, 'builderLicenseNumber': '330105202012100202', 'buildingArea': 21752.0, 'category': '02', 'categoryName': '市政公用工程', 'city': '杭州市', 'completeDate': '2023-02-04', 'contractorCorpNames': '中国建筑第八工程局有限公司', 'county': '拱墅区', 'govOrgId': 5, 'invest': 61000.0, 'lat': 30.39486, 'lng': 120.19172, 'orgName': '市本级', 'projectArea': '浙江省杭州市拱墅区半山街道', 'projectCode': '330105210107020001', 'projectId': 8017, 'projectName': '杭州市城北净水厂工程（一期）', 'projectStatus': '003', 'projectStatusName': '在建', 'province': '浙江省', 'small': 0, 'startDate': '2021-01-19', 'street': '半山街道'}]



# print(list[0].keys())  # 提取key
# list[0]=tuple(list[0].values())
# list1 = print tuple(list[0])
# print(list[0])
def insert_mult_data():
    for i in range(len(list)):
        tup1 = ()
        tup2 = ()
        list1 = ["address", "areaId", "builderLicenseNumber", "buildingArea", "category", "categoryName", "city",
                 "completeDate", "contractorCorpNames", "county", "govOrgId", "invest", "lat", "lng", "orgName",
                 "projectArea", "projectCode", "projectId", "projectName", "projectStatus", "projectStatusName",
                 "province",
                 "small", "startDate", "street"]
        for key in list1:
            if key in list[i].keys():
                tup2 = (list[i][key],)
                # print(type(tup2))
            else:
                tup2 = ("",)
            tup1 = tup1 + tup2
        list[i] = tup1
        # list[i] = tuple(list[i])  # value
        # print((list[i]))
    sql = '''insert into Project (
        address,
        areaId,
        builderLicenseNumber,
        buildingArea,
        category,
        categoryName,
        city,
        completeDate,
        contractorCorpNames,
        county,
        govOrgId,
        invest,
        lat,
        lng,
        orgName,
        projectArea,
        projectCode,
        projectId,
        projectName,
        projectStatus,
        projectStatusName,
        province,
        small,
        startDate,
        street)
        values(
        ?,?,?,?,?,?,?,?,
        ?,?,?,?,?,?,?,?,
        ?,?,?,?,?,?,?,?,?
        )   -- 元组
        '''
    # 构建一个元组
    conn = get_db_conn(db_file)
    cur = conn.cursor()  # 创建游标
    cur.executemany(sql, list)  # 执行sql语句
    conn.commit()  # 提交结果
    close_db_conn(cur, conn)
    return cur.rowcount

insert_mult_data()
