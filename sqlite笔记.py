import sqlite3
from sqlite封装 import get_db_conn, close_db_conn
# 数据库文件
db_file = 'test.db'

# 创建数据表
def init_db():
    # 创建数据表
    sql = '''
        create table ls1
        (
        id integer primary key autoincrement,
        name text,
        appid int,
        no1 int,
        time text,
        is1 int 
        )
    '''

    conn = get_db_conn(db_file)  # 打开或创建数据库文件
    cur = conn.cursor()  # 创建游标
    cur.execute(sql)  # 执行sql语句
    conn.commit()  # 提交结果
    close_db_conn(cur,conn)

# 插入数据函数
def insert_score_data():
    data = ('张三111', 32, '成都', 8000)
    sql = '''insert into table1 (name, age, address, salary)
        values(?,?,?,?)'''
    # 构建一个元组

    conn = sqlite3.connect(db_file)  # 打开或创建数据库文件
    cur = conn.cursor()  # 创建游标
    cur.execute(sql, data)  # 执行sql语句
    conn.commit()  # 提交结果
    cur.close()  # 关闭游标
    conn.close()  # 关闭数据库

# 删除数据
def delete_score_data():
    sql = '''delete from table1 where id=?
        '''
    # 构建一个元组
    id = (5,)

    conn = sqlite3.connect(db_file)  # 打开或创建数据库文件
    cur = conn.cursor()  # 创建游标
    cur.execute(sql, id)  # 执行sql语句
    conn.commit()  # 提交结果
    cur.close()  # 关闭游标
    conn.close()  # 关闭数据库

# 修改数据
def update_score_data():
    sql = '''update table1 set age = ?,salary = ? where id =  4
        '''
    # 构建一个元组
    data = (99, 99,)

    conn = sqlite3.connect(db_file)  # 打开或创建数据库文件
    cur = conn.cursor()  # 创建游标
    cur.execute(sql, data)  # 执行sql语句
    conn.commit()  # 提交结果
    cur.close()  # 关闭游标
    conn.close()  # 关闭数据库

# 查询数据
def select_score_all():
    sql = '''select * from table1 where id =  12
    '''


    conn = sqlite3.connect(db_file)  # 打开或创建数据库文件
    cur = conn.cursor()  # 创建游标
    cur.execute(sql)  # 执行sql语句
    print(type(cur.fetchall()))  # 打印所有结果
    cur.close()  # 关闭游标
    conn.close()  # 关闭数据库

# 插入多条数据
# 列表里面是元组
socre_list = [('张三', 32, '成都', 8000),('张三', 32, '成都', 8000),('张三', 32, '成都', 8000),('张三', 32, '成都', 8000),('张三', 32, '成都', 8000),('张三', 32, '成都', 8000)]
def insert_mult_data():
    sql = '''insert into table1 (name, age, address, salary)
        values(?,?,?,?)   -- 元组
        '''
    # 构建一个元组

    conn = get_db_conn(db_file)
    cur = conn.cursor()  # 创建游标
    cur.executemany(sql, socre_list)  # 执行sql语句
    conn.commit()  # 提交结果
    close_db_conn(cur, conn)
    return cur.rowcount
# for row in cursor:
#     print("id=", row[0])
#     print("name=", row[1])
#     print("address=", row[2])
#     print("salary=", row[3], "\n")

init_db()  # 创建表
# insert_score_data()   # 插入语句
# delete_score_data()  # 删除语句
# update_score_data()  # 修改鱼鱼
# select_score_all()  # 查询语句
# print(insert_mult_data())  #批量插入并打印已插入几条数据


