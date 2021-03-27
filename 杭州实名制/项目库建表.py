import sqlite3
conn = sqlite3.connect("hzsmz.db")
c = conn.cursor()

# 创建表的sql语句
sql1 = '''
    create table Project
        (id integer primary key autoincrement,
        address text,
        areaId int,
        builderLicenseNumber text,
        buildingArea text,
        category text,
        categoryName text,
        city text,
        completeDate text,
        contractorCorpNames text,
        county text,
        govOrgId int,
        invest REAL,
        lat REAL,
        lng REAL,
        orgName text,
        projectArea text,
        projectCode text,
        projectId int,
        projectName text,
        projectStatus text,
        projectStatusName text,
        province text,
        small int,
        startDate text,
        street text,
        time text);
'''
cursor = c.execute(sql1)  # 执行sql语句
# for row in cursor:
#     print("id=", row[0])
#     print("name=", row[1])
#     print("address=", row[2])
#     print("salary=", row[3], "\n")
# conn.commit()  # 提交数据库操作，真正生效
conn.close()  # 关闭数据库
print("成功插入数据")