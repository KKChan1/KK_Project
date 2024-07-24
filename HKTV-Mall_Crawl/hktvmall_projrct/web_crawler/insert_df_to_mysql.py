import pandas as pd

"""
以上代码是一个用于将DataFrame中的数据插入数据库表的函数。让我逐步解释它的工作原理：

insertDF(connection, df:pd.DataFrame, table:str)：这是函数的定义，它接受三个参数：
connection：数据库连接对象，用于与数据库建立连接。
df：要插入数据的DataFrame对象。
table：目标数据库表的名称。
tuple_list = []：创建一个空列表 tuple_list，用于存储DataFrame中每一行的数据。
for x in df.head(3).to_numpy():：遍历DataFrame的前三行，将每一行转换为NumPy数组。
tuple_list.append(tuple(x))：将每一行的NumPy数组转换为元组，
并将元组添加到tuple_list列表中。这样做是为了确保每一行的数据以元组的形式存储。
col = ""：创建一个空字符串 col，用于存储列名的字符串。
for item in list(df.columns):：遍历DataFrame的列名列表。
col = col + item + ','：将每个列名添加到col字符串后面，并在列名之间添加逗号分隔符。
col = col[:-1]：去除col字符串末尾的最后一个逗号，以避免在SQL语句中出现多余的逗号。
for row in tuple_list:：遍历存储了每一行数据的元组列表。
print(f"INSERT INTO {table} ({col}) VALUES {row}")：打印生成的SQL插入语句，
其中{table}会被替换为目标表的名称，{col}会被替换为列名字符串，{row}会被替换为当前行的数据元组。
print('-----')：打印分隔线，用于区分不同的插入语句。
总体而言，该函数的目的是将DataFrame中的数据转换为插入语句，并打印出来。
你可以根据实际需求修改该函数，将生成的SQL语句发送给数据库执行插入操作，而不仅仅是打印出来。
"""

def insertDF(connection, df: pd.DataFrame, table: str):
    '''
    insert data from a DF into a database table
    '''
    cursor = connection.cursor()

    # create a list with each row stored in tuple format


    # create the str for the col names
    col = ""
    for item in list(df.columns):
        col = col + item + ','

    col = col[:-1]

    for _, row in df.iterrows():
        values = [value if pd.notnull(value) else None for value in row]
        placeholders = ",".join(["%s"] * len(row))

        try:
            query = f"INSERT INTO {table} ({col}) VALUES ({placeholders})"
            cursor.execute(query, values)

            print(f"INSERT INTO {table} ({col}) VALUES ({placeholders})")
            print('-----')
        except Exception as e:
            print('INSERT failed', e)

    connection.commit()
    cursor.close()