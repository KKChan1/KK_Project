from pymysql import Connection
from hktvmall_projrct.config_data import *
'''
Functionalities to connect to mySQL
'''
"""
以上代码是一个用于连接到MySQL数据库的函数。让我逐步解释它的工作原理：

connect(host: str, datebase: str)：这是函数的定义，它接受两个参数：
host：数据库主机名或IP地址。
datebase：要连接的数据库名称。
connection = Connection(...)：创建一个连接对象 connection，用于与MySQL数据库建立连接。
在这个例子中，使用了MySQL Connector/Python库提供的Connection类。
host="localhost"：指定数据库的主机名为本地主机，也可以是其他主机名或IP地址。
port=3306：指定数据库的端口号，默认为MySQL的标准端口号3306。
user="root"：指定连接数据库的用户名，在这里使用的是"root"。
password="123456"：指定连接数据库的密码，在这里使用的是"123456"。请根据实际情况修改为正确的用户名和密码。
cursor = connection.cursor()：创建一个游标对象 cursor，用于执行SQL语句和获取查询结果。
conn.select_db("py_sql")：选择要连接的数据库。，
print(f'connecting to {host} - {datebase}')：打印连接的主机和数据库名称。
cursor.execute("SELECT version();")：执行一个SQL查询语句，获取数据库的版本信息。
record = cursor.fetchone()：从查询结果中获取一条记录。
print(f"You are connecting to {record}")：打印连接成功后的数据库版本信息。
return connection：返回连接对象 connection，以便在其他代码中可以使用该连接进行数据库操作。
总体而言，该函数的目的是建立与MySQL数据库的连接，并返回一个连接对象，
以便后续可以使用该连接对象执行SQL查询和操作数据库。请确保在使用该函数之前安装了适当的MySQL数据库驱动程序。
"""

def connect(host: str, datebase: str):
    '''
    Connect to mySQL datebase

    return a connection object
    '''

    # create a connection object
    connection = Connection(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
    )

    # create a cursor object
    cursor = connection.cursor()

    # choose datebase
    connection.select_db(MYSQL_DB)  ####

    print(f'connecting to {host} - {datebase}')

    cursor.execute("SELECT version();")

    record = cursor.fetchone()
    print(f"You are connecting to {record}")

    return connection
