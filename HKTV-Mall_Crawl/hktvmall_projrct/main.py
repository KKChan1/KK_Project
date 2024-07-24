import numpy as np
import pandas as pd
import requests
import csv
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import threading

import time
from hktvmall_projrct import read_csv
from hktvmall_projrct.web_crawler import connect_mysql
from hktvmall_projrct.config_data import *

from web_crawler.insert_df_to_mysql import insertDF
from web_crawler.data_clean import *
from web_crawler.hktv_spider import HKTV_Spider



# def spider_wrapper(spider, urls, result):
#     df = spider.spider(urls)
#     # df = df.replace({np.nan: None, 'nan': None})
#     # df = df.where(pd.notnull(df), None)
#     print(df.info())
#
#     result.append(df)


import traceback

# def spider_wrapper2(spider, urls, result2):
#     try:
#         df = spider.spider(urls)
#         # df = df.replace({np.nan: None, 'nan': None})
#         # df = df.where(pd.notnull(df), None)
#         print(df.info())
#         result2.append(df)
#     except Exception as e:
#         print(f"An error occurred in spider_wrapper2: {e}")
#         traceback.print_exc()


def main():
    path = 'C:/pyhton學習冊/learn/hktvmall_projrct/urls_2024_06_18_30000.csv'
    urls = read_csv.read_urls_csv(path)

    print('Running mySQL')
    conn = connect_mysql.connect(MYSQL_HOST, MYSQL_DB)
    print(f' connection : {conn} ')

    # 创建爬虫对象
    spider = HKTV_Spider()
    df1 = spider.spider(urls[2000:4000])

    # 创建共享变量
    # result = []
    # result2 = []

    # 创建线程
    # thread1 = threading.Thread(target=spider_wrapper, args=(spider, urls[50:60], result))
    # thread1.start()

    # 创建线程
    # thread2 = threading.Thread(target=spider_wrapper2, args=(spider, urls[60:70], result2))
    # thread2.start()

    # 等待线程完成
    # thread1.join()
    # thread2.join()

    # 获取爬虫返回的DataFrame对象
    # df1 = result[0]
    # df2 = result2[0]

    df1 = df1.replace({np.nan: None, 'nan': None})
    # df2 = df2.replace({np.nan: None, 'nan': None})
    df1 = df1.where(pd.notnull(df1), None)
    # df2 = df2.where(pd.notnull(df2), None)

    # 对DataFrame进行处理和插入操作
    insertDF(conn, df1, MYSQL_TABLE)
    # insertDF(conn, df2, MYSQL_TABLE)

start_time = time.time()

main()

end_time = time.time()
duration = end_time - start_time

print(f'運行時間{duration}秒')