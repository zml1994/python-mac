import sqlite3
from sqlite3 import Error

# 获取连接
def get_db_conn(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    if conn is not None:
        return conn

# 关闭资源
def close_db_conn(cur,conn):
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()